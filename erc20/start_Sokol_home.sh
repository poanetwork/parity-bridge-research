#!/bin/bash

PARITY_BASE="/home/koal/parity"
RUNNER="parity_Sokol_home.sh"
TASK="Sokol_home"

cd ${PARITY_BASE}/${TASK}

exec screen -d -m -U -t "${TASK}" -S "${TASK}.screen" -h 5000 -L -s ${PARITY_BASE}/${RUNNER}
