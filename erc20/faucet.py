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

bridge_config = load(test_env['bridge_config'])
bridge_db     = load(test_env['bridge_db'])

if (len(sys.argv) in [4, 5]):
    site = sys.argv[1]
    if (site in ['home', 'foreign']):
        IPC_file = bridge_config[site]['ipc']
    else:
       sys.exit('incorrect network alias')
    web3 = Web3(Web3.IPCProvider(IPC_file))
    recipient = web3.toChecksumAddress(sys.argv[2])
    if len(sys.argv) == 4:
        value = web3.toWei(sys.argv[3], 'ether')
    else:
        value = web3.toWei(sys.argv[3], sys.argv[4])
else:
    sys.exit('incorrect number of arguments')

web3 = Web3(Web3.IPCProvider(IPC_file))

gasPrice    = web3.toWei(1, 'gwei')

################################################################################
# Sending ether
################################################################################

tx = {'from': web3.eth.coinbase, 'to': recipient, 'value': value ,'gasPrice': gasPrice}

print("Sending", value, "wei to", recipient, "at", site)

txHash = web3.eth.sendTransaction(tx)
wait_for_transaction_receipt(web3, txHash)

print("TX:", txHash.hex())

sys.exit(0)
