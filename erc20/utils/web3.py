# This module is wrapper for web3.py module

from web3 import Web3, Account
from json import load as jload

def toChecksumAddress(_addr):
    return Web3.toChecksumAddress(_addr)

def connectionToRPCProvider(_rpc_link):
    ch = None
    try:
        ch = Web3(Web3.HTTPProvider(_rpc_link))
    except e:
        pass
    return ch

def decryptPrivateKey(_file, _pwd):
    with open(_file) as keyfile:
        encrypted_key = keyfile.read()
    keyfile.close()
    
    ac_obj = Account()

    decrypted_key = ac_obj.decrypt(encrypted_key, _pwd)
    return ac_obj.privateKeyToAccount(decrypted_key)

def initContractAtAddress(_web3, _file, _address):
    with open(_file) as f:
        contract_abi = jload(f)
    f.close()

    contract_factory = _web3.eth.contract(
        abi = contract_abi,
    )

    return contract_factory(_address)

def fromEther(_value):
    return Web3.toWei(_value, 'ether')

def toEther(_value):
    return Web3.fromWei(_value, 'ether')
