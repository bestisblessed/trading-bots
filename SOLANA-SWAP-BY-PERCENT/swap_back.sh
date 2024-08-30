#!/bin/bash

# const walletAddress = 'C9WLhFLSX1LomVf3DGV4RyVqxqDSNg7BFr8YaTEzCajs'; // your wallet
# const walletAddress = '6ZDdVLFc2CRaPUwUGnfUsmXr32EBWoNaM9Axf5LWUjc6'; // whale 1 wallet
# const walletAddress = 'tnT1pqpvykZ9S3TVQg9pCAi2DT3UGrYoY91DXxejDZL'; // whale 2 wallet

node check_token_price_and_balance.js B4gtR5n7BEMeyWmJfPqamdMRvQ8y7xNWeebFg53Apump
npx ts-node swap_back.ts

# # rm -rf data && mkdir data
# node inspect_wallet.js C9WLhFLSX1LomVf3DGV4RyVqxqDSNg7BFr8YaTEzCajs
# # node inspect_wallet.js C9WLhFLSX1LomVf3DGV4RyVqxqDSNg7BFr8YaTEzCajs

# Define constants
#!/bin/bash

# Define constants
# WALLET_ADDRESS='C9WLhFLSX1LomVf3DGV4RyVqxqDSNg7BFr8YaTEzCajs'
# TOKEN_ADDRESS='B4gtR5n7BEMeyWmJfPqamdMRvQ8y7xNWeebFg53Apump'
# TOKEN_DECIMALS=6

# # Create data directory and run wallet inspection
# rm -rf data && mkdir data
# node inspect_wallet.js $WALLET_ADDRESS

# # Check token price and extract relevant information
# node check_token_price.js $TOKEN_ADDRESS | tee token_info.txt

# # Debugging: Display the content of the token_info.txt
# echo "Token Info Output:"
# cat token_info.txt

# # Parse the token amount and price from the output
# TOKEN_AMOUNT=$(grep "Liquidity:" token_info.txt | awk '{print $2}' | sed 's/\$//')
# TOKEN_PRICE=$(grep "Price:" token_info.txt | awk '{print $2}' | sed 's/\$//')

# # Debugging: Display extracted values
# echo "Extracted Token Amount: $TOKEN_AMOUNT"
# echo "Extracted Token Price: $TOKEN_PRICE"

# # Calculate 90% of the token amount
# PERCENTAGE=0.90
# AMOUNT_TO_SELL=$(echo "$TOKEN_AMOUNT * $PERCENTAGE" | bc)

# # Convert to lamports
# LAMPORTS_AMOUNT=$(echo "$AMOUNT_TO_SELL * 10^$TOKEN_DECIMALS" | bc | awk '{printf "%.0f", $0}')

# # Debugging: Display calculated values
# echo "Amount to sell: $AMOUNT_TO_SELL"
# echo "Amount in lamports: $LAMPORTS_AMOUNT"

# Run the token swap script with the calculated amount
# Uncomment this line when ready to use
# npx ts-node swap_back.ts $LAMPORTS_AMOUNT


# Run the token swap script with the calculated amount
# npx ts-node swap_back.ts $LAMPORTS_AMOUNT
