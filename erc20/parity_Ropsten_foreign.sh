#!/bin/bash

PARITY_EXEC=/opt/parity/parity
PARITY_CONFIG=/home/koal/parity/Ropsten_foreign.toml
#DEBUG_RPC='-l rpc=trace'
EXTRA_CONFIG='--no-ancient-blocks'

exec ${PARITY_EXEC} --config ${PARITY_CONFIG} ${DEBUG_RPC} ${EXTRA_CONFIG}
