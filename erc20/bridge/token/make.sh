#!/bin/bash

solc='/opt/ethereum-go/bin/solc'

contract=$1

if [ "$contract" == "" ]; then
    if [ -L token.sol ]; then
        targetfile=`readlink -f token.sol`
        contract=`basename --suffix='.sol' $targetfile`
    else
        echo "The contract name must be specified"
        exit 1
    fi
fi

rm *.bin
rm *.abi

$solc --abi token.sol -o ./ 2>/dev/null
$solc --optimize --bin token.sol -o ./ 2>/dev/null

ls -1 *.abi | grep -v $contract | xargs rm
ls -1 *.bin | grep -v $contract | xargs rm

exit 0
