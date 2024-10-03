#!/bin/bash

# Run the script once
/Users/neo/.pyenv/shims/python /Users/neo/trading-bots/SOLANA/MY-FINAL-SOLANA-BOT-vREFACTORED/profit_monitor.py >> /Users/neo/trading-bots/SOLANA/MY-FINAL-SOLANA-BOT-vREFACTORED/profit_monitor.log 2>&1

# Wait for 30 seconds
sleep 40

# Run the script again
/Users/neo/.pyenv/shims/python /Users/neo/trading-bots/SOLANA/MY-FINAL-SOLANA-BOT-vREFACTORED/profit_monitor.py >> /Users/neo/trading-bots/SOLANA/MY-FINAL-SOLANA-BOT-vREFACTORED/profit_monitor.log 2>&1
