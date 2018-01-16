#!/opt/anaconda3/bin/python

from web3 import Web3
from web3.utils.transactions import wait_for_transaction_receipt
import json
import sys

_contractName='ForeignBridge'
_abiFile=_contractName+".abi"

_IPC_file = '/home/koal/parity/PoA_foreign/jsonrpc.ipc'
web3 = Web3(Web3.IPCProvider(_IPC_file))
_actor = "0xf3ee321df87781864f46f6464e764c2827fca73b"
_gasPrice = web3.toWei(18, 'gwei')

_txTempl={'from': _actor, 'gasPrice': _gasPrice}

if (len(sys.argv) == 3):
    contractAddress = sys.argv[1]
    erc20ContractAddress = sys.argv[2]
else:
    sys.exit(1)

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

BridgeContract = ContractFactory(contractAddress)

print("Set contract address...")

txHash = BridgeContract.transact(transaction=_txTempl).setTokenAddress(erc20ContractAddress)
wait_for_transaction_receipt(web3, txHash)

sys.exit(0)
