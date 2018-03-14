#!/opt/anaconda3/bin/python

from web3 import Web3
from web3.utils.transactions import wait_for_transaction_receipt
import json
from toml import load
import sys
from random import randint

_tokenName = 'BridgeableToken'
_abiFile = _tokenName+".abi"

test_env_db = '/home/koal/parity/bridge/test_env_db.toml'
try:
    test_env = load(test_env_db)
except:
    sys.exit(1)

bridge_config = load(test_env['bridge_config'])
bridge_db     = load(test_env['bridge_db'])

_IPC_file = bridge_config['foreign']['ipc']
web3 = Web3(Web3.IPCProvider(_IPC_file))

_gasPrice    = bridge_config['transactions']['withdraw_confirm']['gas_price']

tokenContractAddress = web3.toChecksumAddress(test_env['token_contract_address'])

bridgeContractAddress = web3.toChecksumAddress(bridge_db['foreign_contract_address'])

if 'actor_address' in test_env:
    actor = web3.toChecksumAddress(test_env['actor_address'])
else:
    sys.exit("actor is not set in testenv DB")

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

if (len(sys.argv) == 2):
    value = int(sys.argv[1])
else:
    sys.exit(1)

#############################################################################
# MAIN PART STARTED HERE
#############################################################################

TokenContract = ContractFactory(tokenContractAddress)

print("Withdraw", value, "from Foreign bridge")

txTmpl = {'from': actor, 
          'gasPrice': _gasPrice}

txToSend = TokenContract.functions.approveAndCall(bridgeContractAddress, value, b'').buildTransaction(txTmpl)

# This is needed since sendTransaction does not expect this argument parameter and does not skip it by some reason 
txToSend.pop('chainId', None)

txHash = web3.personal.sendTransaction(txToSend, "11")
wait_for_transaction_receipt(web3, txHash)

print("TX:", txHash.hex())

sys.exit(0)
