#!/opt/anaconda3/bin/python

from web3 import Web3
from web3.utils.transactions import wait_for_transaction_receipt
import json
import sys

#_tokenName='MintableToken'
_tokenName='BridgeableToken'
_abiFile=_tokenName+".abi"
_binFile=_tokenName+".bin"

_IPC_file = '/home/koal/parity/PoA_foreign/jsonrpc.ipc'
web3 = Web3(Web3.IPCProvider(_IPC_file))
_actor = "0xf3Ee321Df87781864f46F6464e764c2827FCa73B"
_gasPrice = web3.toWei(18, 'gwei')
_tokenAmount = 100000

_txTempl={'from': _actor, 'gasPrice': _gasPrice}

if (len(sys.argv) == 2):
    bridgeContractAddress = sys.argv[1]
else:
    sys.exit(1)

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
    bytecode = _contractBIN,
)

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

print("Set minting permissions...")

txHash = TokenContract.transact(transaction=_txTempl).setMintAgent(_actor, True)
wait_for_transaction_receipt(web3, txHash)

print("Mint tokens and transfer to the bridge contract " + bridgeContractAddress)

txHash = TokenContract.transact(transaction=_txTempl).mint(bridgeContractAddress, _tokenAmount)
wait_for_transaction_receipt(web3, txHash)

sys.exit(0)
