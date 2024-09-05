# import os
# import json
# import requests
# import datetime
# from dotenv import load_dotenv
# from colorama import init, Fore, Style
# import subprocess  # To run sell_token.py and sell_token_500.py
# from decimal import Decimal  # Use Decimal for high precision

# # Initialize colorama
# init(autoreset=True)

# # Load environment variables from the .env file
# load_dotenv()

# # Get the wallet address from the environment variables
# wallet_address = os.getenv("MY_BOT_WALLET_ADDRESS")

# # Check if the wallet address was loaded correctly
# if not wallet_address:
#     print(Fore.RED + "Error: MY_BOT_WALLET_ADDRESS is not set in the .env file")
#     exit(1)

# # Ensure the data/ directory exists
# data_dir = 'data'
# if not os.path.exists(data_dir):
#     os.makedirs(data_dir)

# # Define the path for the output file (token balances JSON)
# # wallet_address = "7Qq8RTV2ZP3niS1xmrvDf5PemARSJamWk3gVbECP3yaE"  # Example wallet address
# output_path = os.path.join(data_dir, f'{wallet_address}_token_balances.json')
# buy_prices_path = os.path.join(data_dir, 'buy_prices.json')  # Path to your buy prices JSON
# sold_tokens_path = os.path.join(data_dir, 'sold_tokens.json')  # Path to track sold tokens

# # Dexscreener API endpoint for Solana tokens
# dexscreener_api_endpoint = 'https://api.dexscreener.com/latest/dex/tokens'

# # Load the sold tokens if it exists, else create an empty dictionary
# if os.path.exists(sold_tokens_path):
#     with open(sold_tokens_path, 'r') as f:
#         sold_tokens = json.load(f)
# else:
#     sold_tokens = {}

# # print(" ")

# def get_solana_token_data(token_address, buy_price_usd):
#     if token_address.startswith("So1"):
#         print(Fore.RED + f"Skipping token with address starting with 'So1': {token_address}")
#         return
    
#     try:
#         # Make API request to Dexscreener for the Solana token address
#         response = requests.get(f'{dexscreener_api_endpoint}/{token_address}')
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         token_data = response.json()

#         # Generate a timestamp for when the data is fetched
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

#         # Check if token data and pairs exist and are not None
#         if token_data and 'pairs' in token_data and token_data['pairs']:
#             # print(Fore.WHITE + '-' * 50)
#             # print(Fore.CYAN + f"\n  TOKEN ADDRESS: {token_address}")  # Print token address
            
#             # Get the first pair only
#             pair = token_data['pairs'][0]
#             # price_usd = float(pair.get('priceUsd', '0'))  # Get token price in USD
#             price_usd = Decimal(pair.get('priceUsd', '0'))  # Use Decimal for high precision
#             buy_price_usd = Decimal(buy_price_usd)

#             # Calculate price increase
#             if buy_price_usd > 0:
#                 price_increase_percentage = ((price_usd - buy_price_usd) / buy_price_usd) * 100
                

#                 # Check if price has increased by 500% or more
#                 if price_increase_percentage >= 500:
#                     print(Fore.GREEN + f"Price increased by {price_increase_percentage:.2f}%! Triggering sell for 500% increase: {token_address}.")
#                     # Run the sell_token_500.py script
#                     subprocess.run(['python', 'sell_token_500.py', token_address])

#                 # Check if token has already been sold for 50% or 500% increase
#                 if token_address in sold_tokens:
#                     # print(Fore.GREEN + f"Token {token_address} has already been sold at 50% gain, skipping.")
#                     # print(Fore.WHITE + '-' * 50)
#                     return

#                 # Check if price has increased by 50% or more
#                 elif price_increase_percentage >= 50:
#                     print(Fore.GREEN + f"Price increased by {price_increase_percentage:.2f}%! Triggering sell for 50% increase: {token_address}.")
#                     # Run the sell_token.py script
#                     subprocess.run(['python', 'sell_token_100.py', token_address])
#                     sold_tokens[token_address] = {'sell_percentage': 50, 'timestamp': timestamp}  # Add to sold tokens
#                     save_sold_tokens()  # Save the file here after 500% sale

#                 else:
#                     # print(Fore.MAGENTA + f"Price increase is only {price_increase_percentage:.2f}%, not triggering a sell.")
#                     # print(Fore.WHITE + '-' * 50)
#                     pass

#             else:
#                 print(Fore.RED + f"Invalid buy price for {token_address}.")
    
#     except requests.exceptions.RequestException as e:
#         print(Fore.RED + f"Error fetching liquidity data for Solana token address: {token_address}: {e}")

# # Save sold tokens to the sold_tokens.json file
# def save_sold_tokens():
#     with open(sold_tokens_path, 'w') as f:
#         json.dump(sold_tokens, f, indent=4)

# # Load buy prices from buy_prices.json
# if os.path.exists(buy_prices_path):
#     with open(buy_prices_path, 'r') as f:
#         buy_prices = json.load(f)
# else:
#     print(Fore.RED + f"Buy prices file not found: {buy_prices_path}")
#     buy_prices = {}

# # Load the token mint addresses from the previously saved JSON file
# if os.path.exists(output_path):
#     with open(output_path, 'r') as f:
#         token_data = json.load(f)
        
#         # Check if token_data is a list (as in your JSON structure)
#         if isinstance(token_data, list):
#             for token in token_data:
#                 token_address = token.get('mint')
#                 token_symbol = token.get('symbol')  # Extract the symbol for each token
#                 # if token_symbol:
#                     # print(Fore.YELLOW + f"Token Symbol: {token_symbol}")

#                 # Check if we have the buy price for the token
#                 if token_address and token_address in buy_prices:
#                     buy_price_usd = float(buy_prices[token_address].get('price_usd', '0'))
#                     # print(Fore.CYAN + f"Fetching data for token mint address: {token_address}")
#                     get_solana_token_data(token_address, buy_price_usd)
#                 else:
#                     print(Fore.RED + f"No buy price found for token address: {token_address}")
#         else:
#             print(Fore.RED + "Unexpected format in the JSON file. Expected a list.")
# else:
#     print(Fore.RED + f"File not found: {output_path}")
import os
import json
import requests
import datetime
from dotenv import load_dotenv
from colorama import init, Fore, Style
import subprocess  # To run sell_token.py and sell_token_500.py
from decimal import Decimal  # Use Decimal for high precision

# Initialize colorama
init(autoreset=True)

# Load environment variables from the .env file
load_dotenv()

# Get the wallet address from the environment variables
wallet_address = os.getenv("MY_BOT_WALLET_ADDRESS")

# Check if the wallet address was loaded correctly
if not wallet_address:
    print(Fore.RED + "Error: MY_BOT_WALLET_ADDRESS is not set in the .env file")
    exit(1)

# Ensure the data/ directory exists
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Define the path for the output file (token balances JSON)
output_path = os.path.join(data_dir, f'{wallet_address}_token_balances.json')
buy_prices_path = os.path.join(data_dir, 'buy_prices.json')  # Path to your buy prices JSON
sold_tokens_path = os.path.join(data_dir, 'sold_tokens.json')  # Path to track sold tokens

# Dexscreener API endpoint for Solana tokens
dexscreener_api_endpoint = 'https://api.dexscreener.com/latest/dex/tokens'

# Load the sold tokens if it exists, else create an empty dictionary
if os.path.exists(sold_tokens_path):
    with open(sold_tokens_path, 'r') as f:
        sold_tokens = json.load(f)
else:
    sold_tokens = {}

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

        if token_data and 'pairs' in token_data and token_data['pairs']:
            pair = token_data['pairs'][0]
            price_usd = Decimal(pair.get('priceUsd', '0'))  # Use Decimal for high precision
            buy_price_usd = Decimal(buy_price_usd)

            if buy_price_usd > 0:
                price_increase_percentage = ((price_usd - buy_price_usd) / buy_price_usd) * 100

                # Check if the token has already been sold for a 500% increase
                if token_address in sold_tokens and sold_tokens[token_address].get('sell_500_percent', False):
                    # print(Fore.GREEN + f"Token {token_address} has already been sold at 500% gain, skipping.")
                    return

                # Check if price has increased by 500% or more
                if price_increase_percentage >= 500:
                    print(Fore.GREEN + f"Price increased by {price_increase_percentage:.2f}%! Triggering sell for 500% increase: {token_address}.")
                    subprocess.run(['python', 'sell_token_500.py', token_address])
                    sold_tokens[token_address] = {
                        'sell_50_percent': sold_tokens.get(token_address, {}).get('sell_50_percent', False),
                        'sell_500_percent': True, 'timestamp': timestamp
                    }
                    save_sold_tokens()  # Save the file after the 500% sale
                    return

                # Check if the token has already been sold for a 50% increase
                if token_address in sold_tokens and sold_tokens[token_address].get('sell_50_percent', False):
                    # print(Fore.GREEN + f"Token {token_address} has already been sold at 50% gain, skipping.")
                    return

                # Check if price has increased by 50% or more
                elif price_increase_percentage >= 50:
                    print(Fore.GREEN + f"Price increased by {price_increase_percentage:.2f}%! Triggering sell for 50% increase: {token_address}.")
                    subprocess.run(['python', 'sell_token_100.py', token_address])
                    sold_tokens[token_address] = {
                        'sell_50_percent': True,
                        'sell_500_percent': False, 'timestamp': timestamp
                    }
                    save_sold_tokens()  # Save the file here after 50% sale

                else:
                    # print(Fore.MAGENTA + f"Price increase is only {price_increase_percentage:.2f}%, not triggering a sell.")
                    pass
            else:
                print(Fore.RED + f"Invalid buy price for {token_address}.")

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching liquidity data for Solana token address: {token_address}: {e}")

# Save sold tokens to the sold_tokens.json file
def save_sold_tokens():
    with open(sold_tokens_path, 'w') as f:
        json.dump(sold_tokens, f, indent=4)

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

                # Check if we have the buy price for the token
                if token_address and token_address in buy_prices:
                    buy_price_usd = float(buy_prices[token_address].get('price_usd', '0'))
                    get_solana_token_data(token_address, buy_price_usd)
                else:
                    print(Fore.RED + f"No buy price found for token address: {token_address}")
        else:
            print(Fore.RED + "Unexpected format in the JSON file. Expected a list.")
else:
    print(Fore.RED + f"File not found: {output_path}")
