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

keystore = '/home/koal/parity/keys/PoA_home/UTC--2018-01-11T21-55-28Z--8437ae14-1e28-75d3-4512-a60d63dbfb64'

_IPC_file = bridge_config['home']['ipc']
web3 = Web3(Web3.IPCProvider(_IPC_file))
#web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:38545"))

_gasPrice    = bridge_config['transactions']['withdraw_relay']['gas_price']

bridgeContractAddress = web3.toChecksumAddress(bridge_db['home_contract_address'])

if (len(sys.argv) == 2):
    txNum = int(sys.argv[1])
else:
    sys.exit(1)

net_id = int(web3.version.network)
txTmpl = {
          'to': bridgeContractAddress,
          'gas': 30000,
          'gasPrice': _gasPrice,
          'chainId': net_id
         }

with open(keystore) as keyfile:
    encrypted_key = keyfile.read()
    private_key = web3.eth.account.decrypt(encrypted_key, '11')

actor = web3.eth.account.privateKeyToAccount(private_key)

op_num = web3.eth.getTransactionCount(actor.address)

################################################################################
# Preparing batch of transactions to the bridge contract with ether sending
################################################################################

tx_signed = []

for i in range(0, txNum):
    tx = txTmpl.copy()
    tx['nonce'] = op_num + i

    value = web3.toWei(randint(700, 5000), 'szabo')
    tx['value'] = value

    signed = actor.signTransaction(tx)
    tx_signed.append(signed)
    print('NOnce:', tx['nonce'], 'value:', value)

################################################################################
# Sending batch of transactions
################################################################################

for tx in tx_signed: 
    txHash = web3.eth.sendRawTransaction(tx.rawTransaction)
    print('TX:', txHash.hex())

sys.exit(0)
