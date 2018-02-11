#!/opt/anaconda3/bin/python 

from web3 import Web3
#from web3.utils.transactions import wait_for_transaction_receipt

web3 = Web3(Web3.IPCProvider('/home/koal/parity/PoA_home/jsonrpc.ipc'))

signer = web3.toChecksumAddress("0x842eb2142c5aa1260954f07aae39ddee1640c3a7")
sender = web3.toChecksumAddress("0x37a30534da3d53aa1867adde26e114a3161b2b12")

for i in [signer, sender]:
    balance=web3.eth.getBalance(i)
    print(i, ":", web3.fromWei(balance, 'ether'))
