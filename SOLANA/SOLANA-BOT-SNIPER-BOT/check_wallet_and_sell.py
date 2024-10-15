import os
import json
import requests
import datetime
from dotenv import load_dotenv
from colorama import init, Fore, Style
import subprocess  # To run sell_token.py and sell_token_500.py

# Initialize colorama
init(autoreset=True)

# Load environment variables from the .env file
load_dotenv()

# Ensure the data/ directory exists
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Define the path for the output file (token balances JSON)
wallet_address = "7Qq8RTV2ZP3niS1xmrvDf5PemARSJamWk3gVbECP3yaE"  # Example wallet address
output_path = os.path.join(data_dir, f'{wallet_address}_token_balances.json')
buy_prices_path = os.path.join(data_dir, 'buy_prices.json')  # Path to your buy prices JSON

# Dexscreener API endpoint for Solana tokens
dexscreener_api_endpoint = 'https://api.dexscreener.com/latest/dex/tokens'

print(" ")

def get_solana_token_data(token_address, buy_price_usd):
    if token_address.startswith("So1"):
        print(Fore.RED + f"Skipping token with address starting with 'So1': {token_address}")
        return
    
    try:
        # Make API request to Dexscreener for the Solana token address
        response = requests.get(f'{dexscreener_api_endpoint}/{token_address}')
        response.raise_for_status()  # Raise an exception for HTTP errors
        token_data = response.json()

        # Generate a timestamp for when the data is fetched
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Check if token data and pairs exist and are not None
        if token_data and 'pairs' in token_data and token_data['pairs']:
            # print(Fore.WHITE + '-' * 50)
            # print(Fore.CYAN + f"\n  TOKEN ADDRESS: {token_address}")  # Print token address
            
            # Get the first pair only
            pair = token_data['pairs'][0]
            price_usd = float(pair.get('priceUsd', '0'))  # Get token price in USD

            # Calculate price increase
            if buy_price_usd > 0:
                price_increase_percentage = ((price_usd - buy_price_usd) / buy_price_usd) * 100

                # Check if price has increased by 500% or more
                if price_increase_percentage >= 500:
                    print(Fore.GREEN + f"Price increased by {price_increase_percentage:.2f}%! Triggering sell for 500% increase: {token_address}.")
                    # Run the sell_token_500.py script
                    subprocess.run(['python', 'sell_token_500.py', token_address])

                # Check if price has increased by 75% or more
                elif price_increase_percentage >= 75:
                    print(Fore.GREEN + f"Price increased by {price_increase_percentage:.2f}%! Triggering sell for 75% increase: {token_address}.")
                    # Run the sell_token.py script
                    subprocess.run(['python', 'sell_token_100.py', token_address])

                else:
                    print(Fore.MAGENTA + f"Price increase is only {price_increase_percentage:.2f}%, not triggering a sell.")
                    print(Fore.WHITE + '-' * 50)
            else:
                print(Fore.RED + f"Invalid buy price for {token_address}.")
    
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching liquidity data for Solana token address: {token_address}: {e}")

# Load buy prices from buy_prices.json
if os.path.exists(buy_prices_path):
    with open(buy_prices_path, 'r') as f:
        buy_prices = json.load(f)
else:
    print(Fore.RED + f"Buy prices file not found: {buy_prices_path}")
    buy_prices = {}

# Load the token mint addresses from the previously saved JSON file
if os.path.exists(output_path):
    with open(output_path, 'r') as f:
        token_data = json.load(f)
        
        # Check if token_data is a list (as in your JSON structure)
        if isinstance(token_data, list):
            for token in token_data:
                token_address = token.get('mint')
                token_symbol = token.get('symbol')  # Extract the symbol for each token
                if token_symbol:
                    print(Fore.YELLOW + f"Token Symbol: {token_symbol}")

                # Check if we have the buy price for the token
                if token_address and token_address in buy_prices:
                    buy_price_usd = float(buy_prices[token_address].get('price_usd', '0'))
                    print(Fore.CYAN + f"Fetching data for token mint address: {token_address}")
                    get_solana_token_data(token_address, buy_price_usd)
                else:
                    print(Fore.RED + f"No buy price found for token address: {token_address}")
        else:
            print(Fore.RED + "Unexpected format in the JSON file. Expected a list.")
else:
    print(Fore.RED + f"File not found: {output_path}")
