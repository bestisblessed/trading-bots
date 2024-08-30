#/bin/bash
# Usage: ./runBot.sh <wallet address to monitor>
# Ex) ./runBot.sh 6ZDdVLFc2CRaPUwUGnfUsmXr32EBWoNaM9Axf5LWUjc6

# Hard code whale 1 wallet for first model simplicity
# CRON JOB LINE (every 30 seconds)
# USE .SH AS CRON JOB FILE
# */30 * * * * /path/to/node /path/to/your/script.js <walletAddress>

#ts-node check_wallet.ts 6ZDdVLFc2CRaPUwUGnfUsmXr32EBWoNaM9Axf5LWUjc6
npx ts-node monitor_wallet.ts 6ZDdVLFc2CRaPUwUGnfUsmXr32EBWoNaM9Axf5LWUjc6

# Check if updated_tokens.json exists in the data directory
# Add logic for buying or selling
if [ -f "./data/updated_tokens.json" ]; then
    echo "updated_tokens.json exists, running follow-up script..."
    python swap.py
    # rm data/updated_tokens.json
else
    echo "No updates found, follow-up script will not run."
fi