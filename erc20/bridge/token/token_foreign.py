#!/opt/anaconda3/bin/python

from web3 import Web3
from web3.utils.transactions import wait_for_transaction_receipt
import json
from toml import load, dump
import sys

#_tokenName='MintableToken'
_tokenName = 'BridgeableToken'
_abiFile = _tokenName+".abi"
_binFile = _tokenName+".bin"

test_env_db = '/home/koal/parity/bridge/test_env_db.toml'
try:
    test_env = load(test_env_db)
except:
    test_env = {}

bridge_config = load('/home/koal/parity/bridge/erc20.toml')
bridge_db     = load('/home/koal/parity/bridge/erc20_db.toml')

_IPC_file = bridge_config['foreign']['ipc']
web3 = Web3(Web3.IPCProvider(_IPC_file))

_actor       = web3.toChecksumAddress(bridge_config['foreign']['account'])
_gasPrice    = bridge_config['transactions']['foreign_deploy']['gas_price']
_tokenAmount = 100000
_txTempl={'from': _actor, 'gasPrice': _gasPrice}

bridgeContractAddress = web3.toChecksumAddress(bridge_db['foreign_contract_address'])

#----------------------------------------------------------------------------
# Read ABI
#----------------------------------------------------------------------------
with open(_abiFile) as f:
    _contractABI=json.load(f)
f.close()
#print(_contractABI[0])

#----------------------------------------------------------------------------
# Read Bin
#----------------------------------------------------------------------------
with open(_binFile) as f:
    _contractBIN=f.readline().strip()
f.close()
#print(len(_contractBIN))

ContractFactory = web3.eth.contract(
    abi = _contractABI,
    bytecode = _contractBIN
)

#############################################################################
# MAIN PART STARTED HERE
#############################################################################

# Assuminng that the account is unlocked and script is run on the same
# machine where validator is run.
#web3.personal.unlockAccount(actor, "11", 30)

print("Token contract deployment...")

# Contract Factory deploys contracts but do not link them with a python object
txHash = ContractFactory.deploy(transaction=_txTempl)
wait_for_transaction_receipt(web3, txHash)

# get the contract address
contractAddress = web3.eth.getTransactionReceipt(txHash)['contractAddress']
print("Contract address:", contractAddress)

TokenContract = ContractFactory(contractAddress)

# delegate rights to mint tokens
print("Set minting permissions...")

txHash = TokenContract.transact(transaction=_txTempl).setMintAgent(_actor, True)
wait_for_transaction_receipt(web3, txHash)

# mint few tokens
print("Mint tokens and transfer to the bridge contract " + bridgeContractAddress)

txHash = TokenContract.transact(transaction=_txTempl).mint(bridgeContractAddress, _tokenAmount)
wait_for_transaction_receipt(web3, txHash)

# Store test environment configuration only in case of successful setup
test_env['token_contract_address'] = contractAddress
with open(test_env_db, 'w') as f:
    dump(test_env, f)
f.close()

sys.exit(0)
