#!/bin/bash

# Load the environment variables from the .env file
export $(grep -v '^#' .env | xargs)

# Echo the wallet being used to verify if the env variable is loaded correctly
echo "Using wallet: $MY_BOT_WALLET_ADDRESS"

# Define the tmux session name
SESSION_NAME="SNIPER-BOT"

# Kill the session if it already exists
tmux kill-session -t $SESSION_NAME 2>/dev/null

# Create a new tmux session and run the commands, using the already loaded environment variables
tmux new-session -d -s $SESSION_NAME "echo 'Using wallet: $MY_BOT_WALLET_ADDRESS'; python check_wallet_and_log_buy_prices.py; node SCANNER-PUMP.js"

# Notify the user that the tmux session has been started
echo "tmux session $SESSION_NAME started"

# Attach
tmux attach -t $SESSION_NAME
