#!/bin/bash
rm rug-detections/*
# rm rug-detections-rugcheckxyz/*
rm rankings/*
rm new_tokens/*
rm wallets/*

python monitor_wallet.py

# Start a new screen session called 'bot' and run node SCANNER.js
screen -S bot -dm bash -c 'node SCANNER.js | tee -a scanner.log'

echo "Started 'bot' screen session. You can view it by running: screen -r bot"
