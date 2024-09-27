#!/bin/bash

# Check if an argument is provided
if [ -z "$1" ]; then
  echo "Error: No mint address provided."
  echo "Usage: ./your_script.sh <mint_address>"
  exit 1
fi

# Assign the first argument to the variable 'mint_address'
mint_address=$1

python rug_detector.py $mint_address