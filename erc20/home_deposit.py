#!/opt/anaconda3/bin/python

from utils.getenv import BridgeEnv
from sys import argv, exit
from utils.web3 import fromEther, toEther

tx_num = 1
tx_value = None

# The command can be used with 2 parameters:
# #1 - number of transactions
# #2 - value to transact
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

web3 = b.connectionToHome()
b.initHomeBridgeContract()

gas_price = b.home_bridge.functions.gasPrice().call()
gas_limit = 50000
net_id = int(web3.version.network)

op_num = web3.eth.getTransactionCount(b.actor_address)

tx_templ = {
             'to': b.home_bridge_address,
             'gas': gas_limit,
             'gasPrice': gas_price,
             'chainId': net_id
           }

actor = b.activateActor()
op_num = web3.eth.getTransactionCount(actor.address)

if tx_value == None:
    tx_value = b.home_bridge.functions.minPerTx().call()

################################################################################
# Preparing batch of transactions to the bridge contract with ether sending
################################################################################

tx_signed = []

for i in range(0, tx_num):
    tx = tx_templ.copy()
    tx['nonce'] = op_num + i

    tx['value'] = tx_value

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
