#!/bin/bash
# ./swap_back.sh <mint address> <percentage of holdings to sell>

# Check if the mint address is provided
if [ -z "$1" ]; then
  echo "Error: No mint address provided."
  echo "Usage: ./swap_back.sh <mint address> <percentage of holdings to sell>"
  exit 1
fi

# Check if the percentage of holdings is provided
if [ -z "$2" ]; then
  echo "Error: No percentage of holdings provided."
  echo "Usage: ./swap_back.sh <mint address> <percentage of holdings to sell>"
  exit 1
fi

# Check if the percentage is a valid number between 0 and 100
if ! [[ "$2" =~ ^[0-9]+([.][0-9]+)?$ ]] || (( $(echo "$2 <= 0" | bc -l) )) || (( $(echo "$2 > 100" | bc -l) )); then
  echo "Error: Percentage must be a number between 0 and 100."
  echo "Usage: ./swap_back.sh <mint address> <percentage of holdings to sell>"
  exit 1
fi

# Proceed with the swap
# node check_token_price_and_balance.js $1
# wait $!
# sleep 5
npx ts-node swap_back.ts $1 $2