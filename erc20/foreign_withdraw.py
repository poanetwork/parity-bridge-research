#!/opt/anaconda3/bin/python

from utils.getenv import BridgeEnv
from sys import argv, exit
from utils.web3 import fromEther, toEther

tx_num = 1
tx_value = None

# The command can be used with 2 parameters:
# #1 - number of transactions
# #2 - value to withdraw
if (len(argv) == 2):
    tx_num = int(argv[1])
else:
    if (len(argv) == 3):
         tx_num = int(argv[1])
         tx_value = fromEther(float(argv[2]))
    elif (len(argv) != 1):
        exit("Incorrect number of input parameters")

b = BridgeEnv()
b.initEnv()

web3 = b.connectionToForeign()
b.initForeignBridgeContract()
b.initForeignTokenContract()

gas_price = b.foreign_bridge.functions.gasPrice().call()
gas_limit = 120000
net_id = int(web3.version.network)

if tx_value == None:
    tx_value = b.foreign_bridge.functions.minPerTx().call()

data = b.foreign_token.encodeABI('transferAndCall', (b.foreign_bridge_address, tx_value, b''))

tx_templ = {
             'to': b.foreign_token_address,
             'gas': gas_limit,
             'gasPrice': gas_price,
             'chainId': net_id,
             'value': 0,
             'data': data
           }

actor = b.activateActor()
op_num = web3.eth.getTransactionCount(actor.address)

################################################################################
# Preparing batch of transactions to the bridge contract with tokens withdrawals
################################################################################

tx_signed = []

for i in range(0, tx_num):
    tx = tx_templ.copy()
    tx['nonce'] = op_num + i

    signed = actor.signTransaction(tx)
    tx_signed.append(signed)
    print('NOnce:', tx['nonce'], 'value:', toEther(tx_value))

################################################################################
# Sending batch of transactions
################################################################################

for tx in tx_signed: 
    txHash = web3.eth.sendRawTransaction(tx.rawTransaction)
    print('TX:', txHash.hex())

exit(0)
