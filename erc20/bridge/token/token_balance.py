#!/opt/anaconda3/bin/python

from web3 import Web3
import json
from toml import load
import sys

#_tokenName='MintableToken'
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

tokenContractAddress = web3.toChecksumAddress(test_env['token_contract_address'])

addresses = [web3.toChecksumAddress(bridge_db['foreign_contract_address'])]
if 'actor_address' in test_env:
    addresses.append(web3.toChecksumAddress(test_env['actor_address']))

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

#############################################################################
# MAIN PART STARTED HERE
#############################################################################

TokenContract = ContractFactory(tokenContractAddress)

for i in addresses:
    balance = TokenContract.functions.balanceOf(i).call()
    print(i, ":", balance)

sys.exit(0)
