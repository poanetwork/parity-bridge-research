# This module initializes data to work in the bridge envirionment

from toml import load
from os.path import isfile
from os import getenv
from dotenv import load_dotenv
from json import load as jload

from utils.web3 import (
    toChecksumAddress,
    connectionToRPCProvider,
)

class BridgeEnv():

    def _fromEnv(self):
        self.home_rpc_provider = getenv("HOME_RPC_URL")
        self.foreign_rpc_provider = getenv("FOREIGN_RPC_URL")
        self.home_bridge = toChecksumAddress(getenv("HOME_BRIDGE_ADDRESS"))
        self.foreign_bridge = toChecksumAddress(getenv("FOREIGN_BRIDGE_ADDRESS"))
        self.validator = toChecksumAddress(getenv("VALIDATOR_ADDRESS"))

        return True

    def _fromToml(self, _conf):
        self.home_rpc_provider = _conf["home"]["rpc_host"] + ":" + str(_conf["home"]["rpc_port"])
        self.foreign_rpc_provider = _conf["foreign"]["rpc_host"] + ":" + str(_conf["foreign"]["rpc_port"])
        # Assuming that the validator is the same for both sides of bridge
        self.validator = toChecksumAddress(_conf["foreign"]["account"])

        try:
            db = load(self.test_env["bridge_db"])
        except:
            return False
        
        self.home_bridge = toChecksumAddress(db["home_contract_address"])
        self.foreign_bridge = toChecksumAddress(db["foreign_contract_address"])

        return True

    def _getActorAddress(self):
        try:
            with open(self.test_env["actor_keystore"]) as f:
                ks = jload(f)
            f.close()
        except:
            return False

        self.actor_address = toChecksumAddress("0x" + ks["address"])

        return True


    def initEnv(self, _environment=None):
        if _environment:
            f = _environment
        else:
            f = 'bridge/test_env_db.toml'

        try:
            self.test_env = load(f)
        except:
            return (False, "Cannot load " + f)
        
        bridge_config_file = self.test_env['bridge_config']

        if not isfile(bridge_config_file):
            return (False, bridge_config_file + " not found")
        
        config_type = None
        
        try:
            bridge_config = load(bridge_config_file)
            config_type = "toml"
        except:
            try:
                load_dotenv(bridge_config_file)
                config_type = "env"
            except:
                return False

        retval = False

        if not self._getActorAddress():
            return retval
        
        if config_type == "env":
            retval = self._fromEnv()
        else:
            retval = self._fromToml(bridge_config)

        return retval

    def connectionToHome(self):
        self.home_channel = None
        if (self.home_rpc_provider) and (not self.home_channel):
            self.home_channel = connectionToRPCProvider(self.home_rpc_provider)
        return self.home_channel

    def connectionToForeign(self):
        self.foreign_channel = None
        if (self.foreign_rpc_provider) and (not self.foreign_channel):
            self.foreign_channel = connectionToRPCProvider(self.foreign_rpc_provider)
        return self.foreign_channel

