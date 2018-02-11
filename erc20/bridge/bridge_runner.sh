#!/bin/bash

#export RUST_BACKTRACE=1

#export RUST_LOG=all
#export RUST_LOG=error
#export RUST_LOG=warning
#export RUST_LOG=info
export RUST_LOG=debug

exec ./bridge --config erc20.toml --database erc20_db.toml
