#!/opt/anaconda3/bin/python

from web3 import Web3
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

keystore = test_env['actor_keystore']

_IPC_file = bridge_config['home']['ipc']
web3 = Web3(Web3.IPCProvider(_IPC_file))

gasPrice    = bridge_config['transactions']['withdraw_relay']['gas_price']
gasLimit    = 50000

bridgeContractAddress = web3.toChecksumAddress(bridge_db['home_contract_address'])

if (len(sys.argv) == 2):
    txNum = int(sys.argv[1])
else:
    sys.exit(1)

net_id = int(web3.version.network)
txTmpl = {
          'to': bridgeContractAddress,
          'gas': gasLimit,
          'gasPrice': gasPrice,
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

    value = web3.toWei(10, 'szabo')
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
