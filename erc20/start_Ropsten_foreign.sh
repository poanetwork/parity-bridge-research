#!/bin/bash

PARITY_BASE="/home/koal/poa"
TASK="ropsten_foreign"
PARITY_CONFIG="Ropsten_foreign.toml"
TASK_WORK_DIR="${PARITY_BASE}/test"

#DEBUG_RPC='-l rpc=trace'
EXTRA_CONFIG='--no-ancient-blocks'

configdir=`dirname $0`
cd ${configdir}

source start_common.sh

PARITY_BASE="/home/koal/parity"
RUNNER="parity_Ropsten_foreign.sh"
TASK="Ropsten_foreign"

cd ${PARITY_BASE}/${TASK}

exec screen -d -m -U -t "${TASK}" -S "${TASK}.screen" -h 5000 -L -s ${PARITY_BASE}/${RUNNER}
