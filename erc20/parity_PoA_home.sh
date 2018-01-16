#!/bin/bash

PARITY_EXEC=/opt/parity/parity
PARITY_CONFIG=/home/koal/parity/PoA_home.toml
#DEBUG_RPC='-l rpc=trace'
#EXTRA_CONFIG='--jsonrpc-hosts="all" --jsonrpc-cors null'

exec ${PARITY_EXEC} --config ${PARITY_CONFIG} ${DEBUG_RPC} ${EXTRA_CONFIG}
