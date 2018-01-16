#!/opt/anaconda3/bin/python 

from web3 import Web3
#from web3.utils.transactions import wait_for_transaction_receipt

signer = "0xf3ee321df87781864f46f6464e764c2827fca73b"
sender = "0x08c7e1b446520914ba7126325d69fe2863f62413"

web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:48545'))

for i in [signer, sender]:
    balance=web3.eth.getBalance(i)
    print(web3.fromWei(balance, 'ether'))
