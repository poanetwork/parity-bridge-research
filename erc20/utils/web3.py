# This module is wrapper for web3.py module

from web3 import Web3

def toChecksumAddress(_addr):
    return Web3.toChecksumAddress(_addr)

def connectionToRPCProvider(_rpc_link):
    ch = None
    try:
        ch = Web3(Web3.HTTPProvider(_rpc_link))
    except e:
        pass
    return ch
