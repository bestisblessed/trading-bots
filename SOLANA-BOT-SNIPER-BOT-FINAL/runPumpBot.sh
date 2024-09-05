#!/bin/bash

# export $(grep -v '^#' .env | xargs)
# echo "Using wallet: $MY_BOT_WALLET_ADDRESS"

# python check_wallet_and_log_buy_prices.py
# node SCANNER.js

# v2 tmux
# Define the tmux session name
SESSION_NAME="SNIPER-BOT"

# Kill the session if it already exists
tmux kill-session -t $SESSION_NAME 2>/dev/null

# Create a new tmux session and run the commands
tmux new-session -d -s $SESSION_NAME "export \$(grep -v '^#' .env | xargs); echo 'Using wallet: \$MY_BOT_WALLET_ADDRESS'; python check_wallet_and_log_buy_prices.py; node SCANNER-PUMP.js"
echo "tmux session $SESSION_NAME has been started."
tmux attach -t $SESSION_NAME
