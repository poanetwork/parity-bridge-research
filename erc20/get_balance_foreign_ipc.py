#!/opt/anaconda3/bin/python 

from web3 import Web3
#from web3.utils.transactions import wait_for_transaction_receipt

web3 = Web3(Web3.IPCProvider('/home/koal/parity/PoA_foreign/jsonrpc.ipc'))

signer = web3.toChecksumAddress("0xf3ee321df87781864f46f6464e764c2827fca73b")
sender = web3.toChecksumAddress("0x37a30534da3d53aa1867adde26e114a3161b2b12")
#sender = "0x08c7e1b446520914ba7126325d69fe2863f62413"

for i in [signer, sender]:
    balance=web3.eth.getBalance(i)
    print(i, ":", web3.fromWei(balance, 'ether'))
