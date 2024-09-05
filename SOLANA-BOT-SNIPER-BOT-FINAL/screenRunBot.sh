#!/bin/bash

# Define the screen session name
SESSION_NAME="SNIPER-BOT"

# Kill the session if it already exists
screen -S $SESSION_NAME -X quit 2>/dev/null

# Create a new screen session and run the commands in the background
screen -dmS $SESSION_NAME bash -c "export \$(grep -v '^#' .env | xargs); echo 'Using wallet: \$MY_BOT_WALLET_ADDRESS'; python check_wallet_and_log_buy_prices.py; node SCANNER.js; exec bash"

# Print a message indicating the session is running
echo "Screen session $SESSION_NAME has been started and is running in the background."

screen -r $SESSION_NAME
