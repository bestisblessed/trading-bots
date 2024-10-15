# import os
# from dotenv import load_dotenv
# from moralis import sol_api

# # Load environment variables from the .env file
# load_dotenv()

# # Get the API key from the environment variables
# api_key = os.getenv("MORALIS_API_KEY")

# # wallet_address_input = input("Enter wallet to check: ")
# wallet_address_input = 'BhBigMUkEqwuQAEmYyNpL6jP4sR7DG6umAKtAc8ittiC'

# # Define the parameters with the Solana wallet address and network
# params = {
#     "address": wallet_address_input,
#     "network": "mainnet",
# }

# # Fetch the portfolio balance
# result = sol_api.account.get_portfolio(
#     api_key=api_key,
#     params=params,
# )

# # Print the native SOL balance
# native_balance = result.get('nativeBalance', {})
# print(f"SOL Balance: {native_balance.get('solana', '0')} SOL")

# # Print the token balances in a more organized format
# tokens = result.get('tokens', [])
# print("\nToken Balances:")
# for token in tokens:
#     name = token.get('name', 'Unknown')
#     symbol = token.get('symbol', 'Unknown')
#     amount = token.get('amount', '0')
#     mint = token.get('mint', 'Unknown')
#     print(f"Token: {name} ({symbol})")
#     print(f"  Mint Address: {mint}")
#     print(f"  Balance: {amount}\n")
import os
import json
import sys
from dotenv import load_dotenv
from moralis import sol_api

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv("MORALIS_API_KEY")

# Replace input with a fixed wallet address for this example
# wallet_address_input = 'BhBigMUkEqwuQAEmYyNpL6jP4sR7DG6umAKtAc8ittiC'
if len(sys.argv) > 1:
    wallet_address_input = sys.argv[1]
else:
    print("Usage: python inspect_wallet.py <wallet_address>")
    sys.exit(1)

# Define the parameters with the Solana wallet address and network
params = {
    "address": wallet_address_input,
    "network": "mainnet",
}

# Fetch the portfolio balance
result = sol_api.account.get_portfolio(
    api_key=api_key,
    params=params,
)

# Prepare data to be saved in JSON format
output_data = {
    "wallet_address": wallet_address_input,
    "sol_balance": result.get('nativeBalance', {}).get('solana', '0'),
    "tokens": []
}

# Collect the native SOL balance
print(f"SOL Balance: {output_data['sol_balance']} SOL")

# Collect the token balances
tokens = result.get('tokens', [])
print("\nToken Balances:")
for token in tokens:
    token_data = {
        "name": token.get('name', 'Unknown'),
        "symbol": token.get('symbol', 'Unknown'),
        "amount": token.get('amount', '0'),
        "mint": token.get('mint', 'Unknown')
    }
    output_data["tokens"].append(token_data)
    
    print(f"Token: {token_data['name']} ({token_data['symbol']})")
    print(f"  Mint Address: {token_data['mint']}")
    print(f"  Balance: {token_data['amount']}\n")

# Ensure the data directory exists
data_dir = './data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Save the output data to a JSON file
json_file_name = f"./data/{wallet_address_input}_balance.json"
with open(json_file_name, 'w') as json_file:
    json.dump(output_data, json_file, indent=4)

print(f"Output saved to {json_file_name}")

