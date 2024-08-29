#!/bin/bash

# const walletAddress = 'C9WLhFLSX1LomVf3DGV4RyVqxqDSNg7BFr8YaTEzCajs'; // your wallet
# const walletAddress = '6ZDdVLFc2CRaPUwUGnfUsmXr32EBWoNaM9Axf5LWUjc6'; // whale 1 wallet
# const walletAddress = 'tnT1pqpvykZ9S3TVQg9pCAi2DT3UGrYoY91DXxejDZL'; // whale 2 wallet

# Check if a wallet address was provided as an argument
if [ -z "$1" ]; then
  echo "Error: No wallet address provided."
  echo "Usage: ./run.sh <wallet_address>"
  exit 1
fi

WALLET_ADDRESS=$1

rm -rf data && mkdir data
node inspect_wallet.js $WALLET_ADDRESS
node inspect_token_details_advanced.js $WALLET_ADDRESS
