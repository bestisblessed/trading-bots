import os
from dotenv import load_dotenv
from moralis import sol_api

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv("MORALIS_API_KEY")

wallet_address_input = input("Enter wallet to check: ")

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
    amount_raw = token.get('amountRaw')
    mint = token.get('mint', 'Unknown')
    associated_token_address = token.get('associatedTokenAddress')
    print(f"Token: {name} ({symbol})")
    print(f"  Mint Address: {mint}")
    print(f"  Associated Token Address: {associated_token_address}")
    print(f"  Balance: {amount}")
    print(f"  Balance Raw: {amount_raw}\n")
