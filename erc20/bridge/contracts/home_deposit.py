#!/opt/anaconda3/bin/python

from web3 import Web3
from web3.utils.transactions import wait_for_transaction_receipt
import json
from toml import load
import sys
from random import randint

test_env_db = '/home/koal/parity/bridge/test_env_db.toml'
try:
    test_env = load(test_env_db)
except:
    sys.exit(1)

bridge_config = load('/home/koal/parity/bridge/erc20.toml')
bridge_db     = load('/home/koal/parity/bridge/erc20_db.toml')

_IPC_file = bridge_config['home']['ipc']
web3 = Web3(Web3.IPCProvider(_IPC_file))
#web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:38545"))

_gasPrice    = bridge_config['transactions']['withdraw_relay']['gas_price']

bridgeContractAddress = web3.toChecksumAddress(bridge_db['home_contract_address'])
if 'actor_address' in test_env:
    actor = web3.toChecksumAddress(test_env['actor_address'])
else:
    sys.exit("actor is not set in testenv DB")

################################################################################
# Sending ether to the bridge contract
################################################################################

value = web3.toWei(randint(700, 5000), 'szabo')
tx = {'from': actor, 'to': bridgeContractAddress, 'value': value ,'gasPrice': _gasPrice}

print("Sending", value, "to Home bridge")

txHash = web3.personal.sendTransaction(tx, "11")
wait_for_transaction_receipt(web3, txHash)

print("TX:", txHash.hex())

sys.exit(0)
