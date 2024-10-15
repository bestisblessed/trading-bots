#!/bin/bash

# Define the wallet addresses
WALLET_BOT_1="C9WLhFLSX1LomVf3DGV4RyVqxqDSNg7BFr8YaTEzCajs" # solana bot 1
WALLET_WHALE_1="6ZDdVLFc2CRaPUwUGnfUsmXr32EBWoNaM9Axf5LWUjc6" # whale 1
WALLET_WHALE_2="tnT1pqpvykZ9S3TVQg9pCAi2DT3UGrYoY91DXxejDZL" # whale 2 
WALLET_WHALE_3="BhBigMUkEqwuQAEmYyNpL6jP4sR7DG6umAKtAc8ittiC" # whale 3
WALLET_WHALE_4="tnT1pqpvykZ9S3TVQg9pCAi2DT3UGrYoY91DXxejDZL" # whale 4

# Check if a wallet address is provided
if [ -z "$1" ]; then
    echo "Usage: ./run.sh <wallet address>"
    echo "Available wallet addresses:"
    echo "WALLET_BOT_1: $WALLET_BOT_1"
    echo "WALLET_WHALE_1: $WALLET_WHALE_1"
    echo "WALLET_WHALE_2: $WALLET_WHALE_2"
    echo "WALLET_WHALE_3: $WALLET_WHALE_3"
    echo "WALLET_WHALE_4: $WALLET_WHALE_4"
    exit 1 # Exit the script with a non-zero status to indicate an error
fi

# Create the data directory if it doesn't exist
rm -rf data && mkdir data

# Run the node scripts with the selected wallet address
# node inspect_wallet.js $1
python inspect_wallet.py $1
node inspect_token_details.js $1
