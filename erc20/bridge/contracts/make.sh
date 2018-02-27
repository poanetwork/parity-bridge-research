#!/bin/bash

solc='/opt/ethereum-go/bin/solc'

h_contract="HomeBridge\."
f_contract="ForeignBridge\."

rm *.bin
rm *.abi

$solc --abi bridge.sol -o ./ 2>/dev/null
$solc --optimize --bin bridge.sol -o ./ 2>/dev/null

ls -1 *.abi | grep -v $h_contract | grep -v $f_contract | xargs rm
ls -1 *.bin | grep -v $h_contract | grep -v $f_contract | xargs rm

exit 0
