# import os
# import requests
# import json
# import time
# import subprocess
# from dotenv import load_dotenv
# from colorama import init, Fore

# # Initialize colorama for colored output
# init(autoreset=True)

# # Load environment variables
# load_dotenv()

# # API and wallet details
# api_key = os.getenv("MORALIS_API_KEY")
# wallet_address = os.getenv("MY_BOT_WALLET_ADDRESS")

# # API endpoint for Dexscreener
# dexscreener_api_endpoint = 'https://api.dexscreener.com/latest/dex/tokens'

# # File paths
# buy_prices_path = 'wallets/buy_prices.json'

# # Load the token list from your buy_prices.json file
# if not os.path.exists(buy_prices_path):
#     print(f"Error: {buy_prices_path} not found.")
#     exit(1)

# with open(buy_prices_path, 'r') as f:
#     buy_prices = json.load(f)

# # Function to monitor the token prices and trigger sells
# def monitor_prices():
#     while True:
#         for token_address, token_info in buy_prices.items():
#             try:
#                 response = requests.get(f'{dexscreener_api_endpoint}/{token_address}')
#                 response.raise_for_status()
#                 token_data = response.json()

#                 if 'pairs' in token_data and len(token_data['pairs']) > 0:
#                     current_price = float(token_data['pairs'][0]['priceUsd'])
#                     buy_price = float(token_info['price_usd'])
#                     profit_loss_percent = ((current_price - buy_price) / buy_price) * 100

#                     print(Fore.YELLOW + f"Checking {token_info['name']} ({token_info['symbol']}): "
#                                         f"Profit/Loss: {profit_loss_percent:.2f}%")

#                     # Determine if the token qualifies for a sell action based on profit percentage
#                     if profit_loss_percent >= 90 and not token_info.get('sell_90', False):
#                         trigger_sell(token_address, 'sell_token_90.py', profit_loss_percent, "90%")
#                         buy_prices[token_address]['sell_90'] = True

#                     elif profit_loss_percent >= 75 and not token_info.get('sell_75', False):
#                         trigger_sell(token_address, 'sell_token_75.py', profit_loss_percent, "75%")
#                         buy_prices[token_address]['sell_75'] = True

#                     elif profit_loss_percent >= 50 and not token_info.get('sell_50', False):
#                         trigger_sell(token_address, 'sell_token_50.py', profit_loss_percent, "50%")
#                         buy_prices[token_address]['sell_50'] = True

#                     # Save the updated buy_prices with sell statuses to file
#                     with open(buy_prices_path, 'w') as f:
#                         json.dump(buy_prices, f, indent=2)

#             except requests.exceptions.RequestException as e:
#                 print(Fore.RED + f"Error fetching price for {token_info['name']} ({token_info['symbol']}): {e}")
        
#         # Sleep for a set amount of time before checking again (e.g., 5 minutes)
#         time.sleep(300)

# # Function to trigger the sell script
# def trigger_sell(token_address, script_name, profit_loss_percent, threshold):
#     print(Fore.GREEN + f"Triggering sell for {token_address}: {profit_loss_percent:.2f}% profit (Threshold: {threshold})")
#     try:
#         subprocess.run(['python', script_name, token_address], check=True)
#         print(Fore.GREEN + f"Successfully executed {script_name} for {token_address}")
#     except subprocess.CalledProcessError as e:
#         print(Fore.RED + f"Error executing {script_name} for {token_address}: {e.stderr}")

# if __name__ == "__main__":
#     monitor_prices()
import os
import json
import time
from colorama import init, Fore, Style
from dotenv import load_dotenv
import requests
import subprocess

# Initialize colorama for colored terminal output
init(autoreset=True)

# Load environment variables from .env file
load_dotenv()

# Load buy prices from JSON file
# data_dir = 'wallets'
# buy_prices_file = os.path.join(data_dir, 'buy_prices.json')
# Get the absolute path of the current directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set absolute paths for buy_prices.json and sell scripts
buy_prices_file = os.path.join(script_dir, 'wallets', 'buy_prices.json')
sell_token_50_path = os.path.join(script_dir, 'sell_token_50.py')
sell_token_75_path = os.path.join(script_dir, 'sell_token_75.py')
sell_token_90_path = os.path.join(script_dir, 'sell_token_90.py')

if not os.path.exists(buy_prices_file):
    print(Fore.RED + "Error: buy_prices.json file not found")
    exit(1)

with open(buy_prices_file, 'r') as f:
    buy_prices = json.load(f)

# Dexscreener API endpoint for Solana tokens
dexscreener_api_endpoint = 'https://api.dexscreener.com/latest/dex/tokens'

# Helper function to trigger the sell scripts
def trigger_sell(token_address, sell_script, profit_percent, threshold):
    print(Fore.YELLOW + f"PROFIT {profit_percent}%: Executing {sell_script} for {token_address}")
    script_path = os.path.join(os.getcwd(), sell_script)
    subprocess.run(['python', script_path, token_address], check=True)
    print(Fore.GREEN + f"{sell_script} executed successfully for {token_address} at {threshold}% profit")

# Monitor and calculate profits
for token_address, token_info in buy_prices.items():
    try:
        # Make API request to Dexscreener for the Solana token address
        response = requests.get(f'{dexscreener_api_endpoint}/{token_address}')
        response.raise_for_status()
        token_data = response.json()

        if token_data and 'pairs' in token_data and token_data['pairs']:
            current_price_usd = float(token_data['pairs'][0]['priceUsd'])
            buy_price_usd = float(token_info['price_usd'])

            # Calculate profit/loss percentage
            profit_loss_percent = ((current_price_usd - buy_price_usd) / buy_price_usd) * 100
            profit_loss_percent = round(profit_loss_percent, 2)

            # Print profit/loss with colors
            if profit_loss_percent >= 0:
                print(Fore.GREEN + f"Token: {token_info['symbol']}, Profit: {profit_loss_percent}%")
            else:
                print(Fore.RED + f"Token: {token_info['symbol']}, Loss: {profit_loss_percent}%")

            # Check if we should trigger sell_50, sell_75, or sell_90
            if profit_loss_percent >= 90 and not token_info.get('sell_90', False):
                trigger_sell(token_address, 'sell_token_80.py', profit_loss_percent, "90%")
                buy_prices[token_address]['sell_90'] = True

            elif profit_loss_percent >= 75 and not token_info.get('sell_75', False):
                trigger_sell(token_address, 'sell_token_80.py', profit_loss_percent, "75%")
                buy_prices[token_address]['sell_75'] = True

            elif profit_loss_percent >= 50 and not token_info.get('sell_50', False):
                trigger_sell(token_address, 'sell_token.py', profit_loss_percent, "50%")
                buy_prices[token_address]['sell_50'] = True

        else:
            print(Fore.RED + f"No valid price data found for token: {token_info['symbol']}")

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching data for token {token_info['symbol']}: {e}")

# Save the updated buy_prices.json
with open(buy_prices_file, 'w') as f:
    json.dump(buy_prices, f, indent=2)
print(Fore.GREEN + "Updated buy_prices.json file with sell status")

