import os
from dotenv import load_dotenv
from moralis import sol_api

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv("MORALIS_API_KEY")

# Define the parameters with the Solana wallet address and network
params = {
    "address": "C9WLhFLSX1LomVf3DGV4RyVqxqDSNg7BFr8YaTEzCajs",
    "network": "mainnet",
}

# Fetch the portfolio balance
result = sol_api.account.get_portfolio(
    api_key=api_key,
    params=params,
)

# Print the native SOL balance
native_balance = result.get('nativeBalance', {})
print(f"SOL Balance: {native_balance.get('solana', '0')} SOL")

# Print the token balances in a more organized format
tokens = result.get('tokens', [])
print("\nToken Balances:")
for token in tokens:
    name = token.get('name', 'Unknown')
    symbol = token.get('symbol', 'Unknown')
    amount = token.get('amount', '0')
    mint = token.get('mint', 'Unknown')
    print(f"Token: {name} ({symbol})")
    print(f"  Mint Address: {mint}")
    print(f"  Balance: {amount}\n")
