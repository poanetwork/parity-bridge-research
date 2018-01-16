#!/opt/anaconda3/bin/python

from web3 import Web3
from web3.utils.transactions import wait_for_transaction_receipt
import json
import sys
from random import randint

_contractName='ForeignBridge'
_abiFile=_contractName+".abi"

_IPC_file = '/home/koal/parity/PoA_foreign/jsonrpc.ipc'
web3 = Web3(Web3.IPCProvider(_IPC_file))
_actor = "0xf3ee321df87781864f46f6464e764c2827fca73b"
_gasPrice = web3.toWei(18, 'gwei')

_txTempl={'from': _actor, 'gasPrice': _gasPrice}

if (len(sys.argv) == 2):
    contractAddress = sys.argv[1]
    tokensRecipient = "0x554e8f65d58621cbaa1806c96898ea1b1d9c4ec1"
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

tokenAmount = web3.toWei(randint(100, 2000), 'finney')
fakeTxHash = web3.sha3('0x'+tokenAmount.to_bytes(32, byteorder='big').hex())

print("Deposit " + str(tokenAmount) + ' tokens')

txHash = BridgeContract.transact(transaction=_txTempl).deposit(tokensRecipient, tokenAmount, bytes.fromhex(fakeTxHash[2:]))
wait_for_transaction_receipt(web3, txHash)

sys.exit(0)
