#!/opt/anaconda3/bin/python

from web3 import Web3
from web3.utils.transactions import wait_for_transaction_receipt
import json
from toml import load
import sys

_contractName='ForeignBridge'
_abiFile=_contractName+".abi"

test_env_db = '/home/koal/parity/bridge/test_env_db.toml'
try:
    test_env = load(test_env_db)
except:
    sys.exit(1)

bridge_config = load('/home/koal/parity/bridge/erc20.toml')
bridge_db     = load('/home/koal/parity/bridge/erc20_db.toml')

_IPC_file = bridge_config['foreign']['ipc']
web3 = Web3(Web3.IPCProvider(_IPC_file))

_actor       = web3.toChecksumAddress(bridge_config['foreign']['account'])
_gasPrice    = bridge_config['transactions']['foreign_deploy']['gas_price']
_txTempl={'from': _actor, 'gasPrice': _gasPrice}

bridgeContractAddress = web3.toChecksumAddress(bridge_db['foreign_contract_address'])
tokenContractAddress = web3.toChecksumAddress(test_env['token_contract_address'])

#----------------------------------------------------------------------------
# Read ABI
#----------------------------------------------------------------------------
with open(_abiFile) as f:
    _contractABI=json.load(f)
f.close()
#print(_contractABI[0])

ContractFactory = web3.eth.contract(
    abi = _contractABI,
)

# Assuminng that the account is unlocked and script is run on the same
# machine where validator is run.
#web3.personal.unlockAccount(actor, "11", 30)

BridgeContract = ContractFactory(bridgeContractAddress)

print("Set contract address...")

txHash = BridgeContract.functions.setTokenAddress(tokenContractAddress).transact(transaction=_txTempl)
wait_for_transaction_receipt(web3, txHash)

print("Check that new configuration reflected in the contract...")
print("ERC20 token used by bridge:", BridgeContract.functions.erc20token().call())

sys.exit(0)
