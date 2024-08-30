#/bin/bash
# Usage: ./runBot.sh <wallet address to monitor>
# Ex) ./runBot.sh 6ZDdVLFc2CRaPUwUGnfUsmXr32EBWoNaM9Axf5LWUjc6
# Hard code whale 1 wallet for first model simplicity
# CRON JOB LINE (every 30 seconds)
# USE .SH AS CRON JOB FILE
# */30 * * * * /path/to/node /path/to/your/script.js <walletAddress>


#ts-node check_wallet.ts 6ZDdVLFc2CRaPUwUGnfUsmXr32EBWoNaM9Axf5LWUjc6
npx ts-node monitor_wallet.ts 6ZDdVLFc2CRaPUwUGnfUsmXr32EBWoNaM9Axf5LWUjc6

Check if updated_tokens.json exists in the data directory
Add logic for buying or selling
if [ -f "./data/updated_tokens.json" ]; then
    echo "updated_tokens.json exists, running follow-up script..."
    python swap.py
    # rm data/updated_tokens.json
else
    echo "No updates found, follow-up script will not run."
fi

# Check if updated_tokens.json exists in the data directory
# if [ -f "./data/updated_tokens.json" ]; then
#     echo "updated_tokens.json exists, processing changes..."

#     # Process each added token individually
#     added_count=$(jq '.added | length' ./data/updated_tokens.json)
#     if [ "$added_count" -gt 0 ]; then
#         echo "Processing added tokens..."
#         for i in $(seq 0 $(($added_count - 1))); do
#             token_info=$(jq -r ".added[$i]" ./data/updated_tokens.json)
#             echo "Added Token:"
#             echo "$token_info"
#             # You can pass token_info to your TypeScript script if needed
#             # e.g., npx ts-node handle_added_token.ts "$token_info"
#         done
#     fi

#     # Process each removed token individually
#     removed_count=$(jq '.removed | length' ./data/updated_tokens.json)
#     if [ "$removed_count" -gt 0 ]; then
#         echo "Processing removed tokens..."
#         for i in $(seq 0 $(($removed_count - 1))); do
#             token_info=$(jq -r ".removed[$i]" ./data/updated_tokens.json)
#             echo "Removed Token:"
#             echo "$token_info"
#             # You can pass token_info to your TypeScript script if needed
#             # e.g., npx ts-node handle_removed_token.ts "$token_info"
#         done
#     fi

# else
#     echo "No updates found, no tokens to process."
# fi