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
# load_dotenv()

# Load buy prices from JSON file
# data_dir = 'wallets'
# buy_prices_file = os.path.join(data_dir, 'buy_prices.json')
# Get the absolute path of the current directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# # Define the absolute path to the .env file
# env_path = os.path.join(script_dir, '.env')

# # Load the .env file from the absolute path
# load_dotenv(dotenv_path=env_path)

# Get the absolute path to the .env file
env_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.env'))

# Load environment variables from the .env file
load_dotenv(env_file_path)

# Set absolute paths for buy_prices.json and sell scripts
buy_prices_file = os.path.join(script_dir, 'wallets', 'buy_prices.json')
sell_token_50_path = os.path.join(script_dir, 'sell_token_50.py')
sell_token_80_path = os.path.join(script_dir, 'sell_token_80.py')
sell_token_90_path = os.path.join(script_dir, 'sell_token_90.py')
sell_token_100_path = os.path.join(script_dir, 'sell_token_100.py')
sell_token_500_path = os.path.join(script_dir, 'sell_token_500.py')

if not os.path.exists(buy_prices_file):
    print(Fore.RED + "Error: buy_prices.json file not found")
    exit(1)

with open(buy_prices_file, 'r') as f:
    buy_prices = json.load(f)

# Dexscreener API endpoint for Solana tokens
dexscreener_api_endpoint = 'https://api.dexscreener.com/latest/dex/tokens'

# Helper function to trigger the sell scripts
# def trigger_sell(token_address, sell_script, profit_percent, threshold):
#     print(Fore.YELLOW + f"PROFIT {profit_percent}%: Executing {sell_script} for {token_address}")
#     script_path = os.path.join(os.getcwd(), sell_script)
#     subprocess.run(['python', script_path, token_address], check=True)
#     print(Fore.GREEN + f"{sell_script} executed successfully for {token_address} at {threshold}% profit")
def trigger_sell(token_address, sell_script, profit_percent, threshold):
    print(Fore.YELLOW + f"PROFIT {profit_percent}%: Executing {sell_script} for {token_address}")
    script_path = os.path.join(script_dir, sell_script)  # Ensure script_dir points to the correct directory
    subprocess.run(['python', script_path, token_address], check=True)
    print(Fore.GREEN + f"{sell_script} executed successfully for {token_address} at {threshold}% profit")

# Monitor and calculate profits
for token_address, token_info in buy_prices.items():
    # print('')
    try:
        # Make API request to Dexscreener for the Solana token address
        response = requests.get(f'{dexscreener_api_endpoint}/{token_address}')
        response.raise_for_status()
        token_data = response.json()

        # Initialize sell flags if they don't exist
        if 'sell_50' not in token_info:
            token_info['sell_50'] = False
        if 'sell_80' not in token_info:
            token_info['sell_80'] = False
        if 'sell_90' not in token_info:
            token_info['sell_90'] = False
        if 'sell_100' not in token_info:
            token_info['sell_100'] = False
        if 'sell_500' not in token_info:
            token_info['sell_500'] = False

        if token_data and 'pairs' in token_data and token_data['pairs']:
            current_price_usd = float(token_data['pairs'][0]['priceUsd'])
            buy_price_usd = float(token_info['price_usd'])

            # Calculate profit/loss percentage
            profit_loss_percent = ((current_price_usd - buy_price_usd) / buy_price_usd) * 100
            profit_loss_percent = round(profit_loss_percent, 2)

            # Print profit/loss with colors
            if profit_loss_percent >= 0:
                print(Fore.GREEN + f"{token_info['symbol']} {profit_loss_percent}%")
            else:
                print(Fore.RED + f"{token_info['symbol']} {profit_loss_percent}%")

            # Check if we should trigger sell_50, sell_75, or sell_90
            if profit_loss_percent >= 500 and not token_info.get('sell_500', False):
                trigger_sell(token_address, 'sell_token_500.py', profit_loss_percent, "500%")
                buy_prices[token_address]['sell_500'] = True
                token_info['sell_500'] = True
                USER = 'ucdzy7t32br76dwht5qtz5mt7fg7n3'
                API = 'a78cw5vdac5t34g4y1f7zz1gmoxp89'
                message = f"SOLD {token_info['symbol']} 500% Profit - 50% Tokens"
                payload = {"message": message, "user": USER, "token": API}
                r = requests.post('https://api.pushover.net/1/messages.json', data=payload, headers={'User-Agent': 'Python'})
                if not r.status_code == 200:
                    print(r.text)
                time.sleep(8)

            # if profit_loss_percent >= 90 and not token_info.get('sell_90', False):
            #     trigger_sell(token_address, 'sell_token_90.py', profit_loss_percent, "90%")
            #     buy_prices[token_address]['sell_90'] = True
            #     token_info['sell_90'] = True
            #     USER = 'ucdzy7t32br76dwht5qtz5mt7fg7n3'
            #     API = 'a78cw5vdac5t34g4y1f7zz1gmoxp89'
            #     message = f"SOLD 90% of {token_info['symbol']} TOKEN"
            #     payload = {"message": message, "user": USER, "token": API}
            #     r = requests.post('https://api.pushover.net/1/messages.json', data=payload, headers={'User-Agent': 'Python'})
            #     if not r.status_code == 200:
            #         print(r.text)

            # elif profit_loss_percent >= 80 and not token_info.get('sell_80', False):
            #     trigger_sell(token_address, 'sell_token_80.py', profit_loss_percent, "80%")
            #     buy_prices[token_address]['sell_80'] = True
            #     token_info['sell_80'] = True
            #     USER = 'ucdzy7t32br76dwht5qtz5mt7fg7n3'
            #     API = 'a78cw5vdac5t34g4y1f7zz1gmoxp89'
            #     message = f"SOLD 80% of {token_info['symbol']} TOKEN"
            #     payload = {"message": message, "user": USER, "token": API}
            #     r = requests.post('https://api.pushover.net/1/messages.json', data=payload, headers={'User-Agent': 'Python'})
            #     if not r.status_code == 200:
            #         print(r.text)

            elif profit_loss_percent >= 100 and not token_info.get('sell_100', False):
                trigger_sell(token_address, 'sell_token_100.py', profit_loss_percent, "100%")
                buy_prices[token_address]['sell_100'] = True
                token_info['sell_100'] = True
                USER = 'ucdzy7t32br76dwht5qtz5mt7fg7n3'
                API = 'a78cw5vdac5t34g4y1f7zz1gmoxp89'
                message = f"SOLD {token_info['symbol']} 100% Profit - 50% of tokens"
                payload = {"message": message, "user": USER, "token": API}
                r = requests.post('https://api.pushover.net/1/messages.json', data=payload, headers={'User-Agent': 'Python'})
                if not r.status_code == 200:
                    print(r.text)
                time.sleep(8)

            # elif profit_loss_percent >= 50 and not token_info.get('sell_50', False):
            #     trigger_sell(token_address, 'sell_token_50.py', profit_loss_percent, "50%")
            #     buy_prices[token_address]['sell_50'] = True
            #     token_info['sell_50'] = True
            #     USER = 'ucdzy7t32br76dwht5qtz5mt7fg7n3'
            #     API = 'a78cw5vdac5t34g4y1f7zz1gmoxp89'
            #     message = f"SOLD {token_info['symbol']} 50% Profit - 50% of tokens"
            #     payload = {"message": message, "user": USER, "token": API}
            #     r = requests.post('https://api.pushover.net/1/messages.json', data=payload, headers={'User-Agent': 'Python'})
            #     if not r.status_code == 200:
            #         print(r.text)
            #     time.sleep(8)

        else:
            print(Fore.RED + f"No valid price data found for token: {token_info['symbol']}")

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching data for token {token_info['symbol']}: {e}")

# Save the updated buy_prices.json
with open(buy_prices_file, 'w') as f:
    json.dump(buy_prices, f, indent=2)
# print(Fore.GREEN + "Updated buy_prices.json file with sell status")

