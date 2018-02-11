#!/bin/bash

PARITY_BASE="/home/koal/parity/bridge"
RUNNER="bridge_runner.sh"
TASK="PoA_bridge"

cd ${PARITY_BASE}

exec screen -d -m -U -t "${TASK}" -S "${TASK}.screen" -h 5000 -L -s ${PARITY_BASE}/${RUNNER}
