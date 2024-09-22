import os
import requests
import json
from dotenv import load_dotenv
import time
from colorama import Fore, init
init(autoreset=True)

# Load environment variables
load_dotenv()

# API and wallet details
api_key = os.getenv("MORALIS_API_KEY")
wallet_address = os.getenv("MY_BOT_WALLET_ADDRESS")

# API endpoint for Dexscreener
dexscreener_api_endpoint = 'https://api.dexscreener.com/latest/dex/tokens'

# Load the token list from your buy_prices.json file
buy_prices_path = 'wallets/buy_prices.json'

# Ensure the buy prices file exists
if not os.path.exists(buy_prices_path):
    print(f"Error: {buy_prices_path} not found.")
    exit(1)

with open(buy_prices_path, 'r') as f:
    buy_prices = json.load(f)

# To store current prices
current_prices = {}

# Fetch the current prices and store them in current_prices
for token_address, token_info in buy_prices.items():
    try:
        response = requests.get(f'{dexscreener_api_endpoint}/{token_address}')
        response.raise_for_status()  # Check for errors
        token_data = response.json()

        # Extract the price
        if 'pairs' in token_data and len(token_data['pairs']) > 0:
            price_usd = token_data['pairs'][0]['priceUsd']
            current_prices[token_address] = {
                'name': token_info['name'],
                'symbol': token_info['symbol'],
                'price_usd': price_usd,
            }
            print(f"Fetched price for {token_info['name']} ({token_info['symbol']}): {price_usd}")
        else:
            print(f"No price data available for {token_info['name']} ({token_info['symbol']})")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for token {token_info['name']} ({token_info['symbol']}): {e}")

# Save the current prices to a file
current_prices_path = 'wallets/current_prices.json'
if not os.path.exists('wallets'):
    os.makedirs('wallets')

with open(current_prices_path, 'w') as f:
    json.dump(current_prices, f, indent=2)
print(f"Current prices saved to {current_prices_path}")

# Compare buy prices with current prices and calculate profit/loss
for token_address, buy_info in buy_prices.items():
    buy_price = float(buy_info['price_usd'])
    current_info = current_prices.get(token_address)

    if current_info:
        current_price = float(current_info['price_usd'])
        # Calculate profit/loss percentage
        profit_loss_percent = ((current_price - buy_price) / buy_price) * 100

        # Print the result
        if profit_loss_percent >= 0:
            print(Fore.GREEN + f"{buy_info['name']} ({buy_info['symbol']}): +{profit_loss_percent:.2f}% (Profit)")
        else:
            print(Fore.RED + f"{buy_info['name']} ({buy_info['symbol']}): {profit_loss_percent:.2f}% (Loss)")
    else:
        print(f"Current price data not found for {buy_info['name']} ({buy_info['symbol']})")

