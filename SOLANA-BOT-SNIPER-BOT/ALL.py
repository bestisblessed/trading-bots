import os
import json
import requests
import datetime
from dotenv import load_dotenv
from moralis import sol_api
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv("MORALIS_API_KEY")

# Define the parameters with the Solana wallet address and network
params = {
    # "address": "6ZDdVLFc2CRaPUwUGnfUsmXr32EBWoNaM9Axf5LWUjc6",
    # "address": "7Qq8RTV2ZP3niS1xmrvDf5PemARSJamWk3gVbECP3yaE",
    "address": "BhBigMUkEqwuQAEmYyNpL6jP4sR7DG6umAKtAc8ittiC",
    "network": "mainnet",
}

# Fetch the portfolio balance
result = sol_api.account.get_portfolio(
    api_key=api_key,
    params=params,
)

# Extract token balances
tokens = result.get('tokens', [])

# Ensure the data/ directory exists
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Define the path for the output file
wallet_address = params['address']
output_path = os.path.join(data_dir, f'{wallet_address}_token_balances.json')

# Save the current token balances to a JSON file
with open(output_path, 'w') as f:
    json.dump(tokens, f, indent=2)
print(f'Current token balances saved to {output_path}')

# Print the native SOL balance
native_balance = result.get('nativeBalance', {})
print(f"SOL Balance: {native_balance.get('solana', '0')} SOL")

# Print the token balances in a more organized format
print("\nToken Balances:")
for token in tokens:
    name = token.get('name', 'Unknown')
    symbol = token.get('symbol', 'Unknown')
    amount = token.get('amount', '0')
    mint = token.get('mint', 'Unknown')
    associated_token_address = token.get('associatedTokenAddress')
    print(f"Token: {name} ({symbol})")
    print(f"  Mint Address: {mint}")
    print(f"  Associated Token Address: {associated_token_address}")
    print(f"  Balance: {amount}")
    print(" ")
    # print('-' * 50)

# Dexscreener API endpoint for Solana tokens
dexscreener_api_endpoint = 'https://api.dexscreener.com/latest/dex/tokens'

def get_solana_token_data(token_address):
    if token_address.startswith("So1"):
        print(Fore.RED + f"Skipping token with address starting with 'So1': {token_address}")
        return
    
    try:
        # Make API request to Dexscreener for the Solana token address
        response = requests.get(f'{dexscreener_api_endpoint}/{token_address}')
        response.raise_for_status()  # Raise an exception for HTTP errors
        token_data = response.json()

        # Debugging: Print the raw API response to understand what is returned
        # print(Fore.YELLOW + f"API Response for {token_address}: {json.dumps(token_data, indent=2)}")

        # Generate a timestamp for when the data is fetched
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Check if token data and pairs exist and are not None
        if token_data and 'pairs' in token_data and token_data['pairs']:
            print(Fore.WHITE + '-' * 50)
            print(Fore.CYAN + f"\n  TOKEN ADDRESS: {token_address}")  # Print token address
            
            for pair in token_data['pairs']:
                solana_token_name = pair['baseToken']['name']
                solana_token_symbol = pair['baseToken']['symbol']
                solana_token_liquidity = pair['liquidity']['base']
                quote_token_name = pair['quoteToken']['name']
                quote_token_symbol = pair['quoteToken']['symbol']
                quote_token_liquidity = pair['liquidity']['quote']
                usd_liquidity = pair['liquidity']['usd']
                price_usd = pair.get('priceUsd', 'Price not available')  # Get token price in USD

                # Print liquidity and price details
                # print(Fore.WHITE + '-' * 50)
                print(Fore.YELLOW + f"\n  {solana_token_name} ({solana_token_symbol}) / {quote_token_name} ({quote_token_symbol})")
                print(Fore.GREEN + f"  Price (USD): {price_usd}")
                print(Fore.GREEN + f"  Timestamp: {timestamp}")
                print(Fore.GREEN + f"  Liquidity (Solana Token): {solana_token_liquidity}")
                print(Fore.GREEN + f"  Liquidity (Quote Token): {quote_token_liquidity}")
                print(Fore.GREEN + f"  Liquidity (USD): {usd_liquidity}\n")
        else:
            print(Fore.WHITE + '-' * 50)
            print(Fore.RED + f"\nNo liq pairs found for: {token_address}\n")
    
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching liquidity data for Solana token address: {token_address}: {e}")


# Load the token addresses from the previously saved JSON file and check their prices and liquidity
if os.path.exists(output_path):
    with open(output_path, 'r') as f:
        token_data = json.load(f)
        for token in token_data:
            mint_address = token.get('mint')
            if mint_address:
                get_solana_token_data(mint_address)
