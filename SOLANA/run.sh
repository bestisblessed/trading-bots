#!/bin/bash

# Define the wallet addresses
WALLET_ADDRESS_DEFAULT="6ZDdVLFc2CRaPUwUGnfUsmXr32EBWoNaM9Axf5LWUjc6" # whale1 wallet
WALLET_ADDRESS_WHALE2="tnT1pqpvykZ9S3TVQg9pCAi2DT3UGrYoY91DXxejDZL" # whale2 wallet
WALLET_ADDRESS_MINE="C9WLhFLSX1LomVf3DGV4RyVqxqDSNg7BFr8YaTEzCajs"    # my wallet

# Set the wallet address based on the argument or default to whale1
case "$1" in
    mywallet)
        WALLET_ADDRESS="$WALLET_ADDRESS_MINE"
        ;;
    whale1)
        WALLET_ADDRESS="$WALLET_ADDRESS_DEFAULT"
        ;;
    whale2)
        WALLET_ADDRESS="$WALLET_ADDRESS_WHALE2"
        ;;
    "")
        # No argument provided, default to whale1
        WALLET_ADDRESS="$WALLET_ADDRESS_DEFAULT"
        ;;
    *)
        echo "Error: Unknown wallet name '$1'"
        echo "Usage: ./swap.sh [mywallet|whale1|whale2]"
        echo "Defaulting to whale1 wallet address."
        WALLET_ADDRESS="$WALLET_ADDRESS_DEFAULT"
        ;;
esac

# Create the data directory if it doesn't exist
rm -rf data && mkdir data

# Run the node scripts with the selected wallet address
node inspect_wallet.js $WALLET_ADDRESS
node inspect_token_details_advanced.js $WALLET_ADDRESS
