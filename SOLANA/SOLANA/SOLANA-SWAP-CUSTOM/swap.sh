#!/bin/bash
# ./swap.sh <mint address> <amount of sol to buy>

# Check if the SOL amount is provided
if [ -z "$1" ]; then
  echo "Error: No mint address provided."
  echo "Usage: ./swap.sh <mint address> <amount of SOL to buy>"
  exit 1
fi

# Check if the SOL amount is provided
if [ -z "$2" ]; then
  echo "Error: No SOL amount provided."
  echo "Usage: ./swap.sh <mint address> <amount of SOL to buy>"
  exit 1
fi

# Check if the amount of SOL is greater than 0.1
if (( $(echo "$2 > 0.1" | bc -l) )); then
  read -p "You are about to swap $2 SOL. Are you sure? (yes/no): " confirm
  if [ "$confirm" != "yes" ]; then
    echo "Swap aborted."
    exit 1
  fi
fi

# Proceed with the swap
npx ts-node swap.ts $1 $2