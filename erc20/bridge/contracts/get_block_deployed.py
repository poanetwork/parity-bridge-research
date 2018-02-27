#!/opt/anaconda3/bin/python

from web3 import Web3
import json
from toml import load
import sys

_contractName='ForeignBridge'
_abiFile=_contractName+".abi"

bridge_config = load('/home/koal/parity/bridge/erc20.toml')
bridge_db     = load('/home/koal/parity/bridge/erc20_db.toml')

def getBlockNumber(_chain):
    IPC_file = bridge_config[_chain]['ipc']
    web3 = Web3(Web3.IPCProvider(IPC_file))

    bridgeContractAddress = web3.toChecksumAddress(bridge_db[_chain + '_contract_address'])

    #----------------------------------------------------------------------------
    # Read ABI
    #----------------------------------------------------------------------------
    with open(_abiFile) as f:
        _contractABI=json.load(f)
    f.close()

    ContractFactory = web3.eth.contract(
        abi = _contractABI,
    )

    BridgeContract = ContractFactory(bridgeContractAddress)

    print(_chain, "bridge contract deployed at:", BridgeContract.functions.blockDeployed().call())

getBlockNumber('home')
getBlockNumber('foreign')

sys.exit(0)
