import os
import csv
import requests
import datetime
from dotenv import load_dotenv
from colorama import init, Fore
import sys
import time
import subprocess
import json

# Initialize colorama for colored output
init(autoreset=True)

# Load environment variables from the .env file (if needed)
load_dotenv()

# Dexscreener API endpoint for Solana tokens
dexscreener_api_endpoint = 'https://api.dexscreener.com/latest/dex/tokens'

# Create the "rug-detections" directory if it doesn't exist
output_directory = "rug-detections"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def get_solana_token_data(mint_address):
    # Skip tokens starting with "So1" (often Solana native tokens)
    if mint_address.startswith("So1"):
        print(Fore.RED + f"Skipping token with address starting with 'So1': {mint_address}")
        return

    try:
        # Make an API request to Dexscreener for the provided Solana token address
        response = requests.get(f'{dexscreener_api_endpoint}/{mint_address}')
        response.raise_for_status()  # Raise an exception for HTTP errors
        token_data = response.json()

        # Generate a timestamp for when the data is fetched
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Check if token data and pairs exist
        if token_data and 'pairs' in token_data and token_data['pairs']:
            print(Fore.WHITE + '-' * 50)
            print(Fore.CYAN + f"\n  TOKEN ADDRESS: {mint_address}")  # Print token address
            
            # Get the first pair only
            pair = token_data['pairs'][0]
            solana_token_name = pair['baseToken']['name']
            solana_token_symbol = pair['baseToken']['symbol']
            solana_token_liquidity = pair['liquidity']['base']
            quote_token_name = pair['quoteToken']['name']
            quote_token_symbol = pair['quoteToken']['symbol']
            quote_token_liquidity = pair['liquidity']['quote']
            usd_liquidity = pair['liquidity']['usd']
            price_usd = pair.get('priceUsd', 'Price not available')  # Get token price in USD
            # trading_volume_24h = pair.get('volume', {}).get('h24', 'Not available')  # 24h trading volume
            # New info: volume, liquidity changes, and tx counts
            # volume_change = pair.get('volume', {}).get('change', 'Not available')
            # txns_24h = pair.get('txns', {}).get('h24', {}).get('count', 'Not available')  # 24h transaction count
            # price_change_24h = pair.get('priceChange', {}).get('h24', 'Not available')  # Price change in 24h
            # fdv = pair.get('fdv', 'Not available')  # Fully diluted valuation (useful to gauge token's market cap)

            # Print liquidity and price details
            print(Fore.YELLOW + f"\n  {solana_token_name} ({solana_token_symbol}) / {quote_token_name} ({quote_token_symbol})")
            print(Fore.GREEN + f"  Price (USD): {price_usd}")
            print(Fore.GREEN + f"  Timestamp: {timestamp}")
            print(Fore.GREEN + f"  Liquidity (Solana Token): {solana_token_liquidity}")
            print(Fore.GREEN + f"  Liquidity (Quote Token): {quote_token_liquidity}")
            print(Fore.GREEN + f"  Liquidity (USD): {usd_liquidity}")
            # print(Fore.GREEN + f"  Trading Volume (24h): {trading_volume_24h}")
            # print(Fore.GREEN + f"  Volume Change (24h): {volume_change}")
            # print(Fore.GREEN + f"  Transaction Count (24h): {txns_24h}")
            # print(Fore.GREEN + f"  Price Change (24h): {price_change_24h}")
            # print(Fore.GREEN + f"  Fully Diluted Valuation (FDV): {fdv}\n")

            # Rug Pull Indicators
            print('')
            if float(usd_liquidity) < 1000:  # Example threshold
                print(Fore.RED + f"Warning: Very low USD liquidity for {solana_token_symbol} ({usd_liquidity} USD) - Potential rug pull risk.")
            # if int(txns_24h) < 10:
            #     print(Fore.RED + f"Warning: Very low transaction count in the last 24h for {solana_token_symbol}.")
            # if float(price_change_24h) < -50:  # Example: If price dropped over 50%
            #     print(Fore.RED + f"Warning: Significant price drop ({price_change_24h}%) in the last 24h.")

            # Save the data to a CSV file named after the token address
            # csv_file_path = (f"./rug-detections/{mint_address}.csv")
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_directory = os.path.join(script_dir, "rug-detections")
            csv_file_path = os.path.join(output_directory, f"{mint_address}.csv")
            print(csv_file_path)
            with open(csv_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Token Name', 'Token Symbol', 'Quote Token Name', 'Quote Token Symbol', 'Price (USD)', 'Solana Liquidity', 'Quote Liquidity', 'USD Liquidity', 'Timestamp'])
                writer.writerow([solana_token_name, solana_token_symbol, quote_token_name, quote_token_symbol, price_usd, solana_token_liquidity, quote_token_liquidity, usd_liquidity, timestamp])
            print(Fore.GREEN + f"\nData saved to {csv_file_path}")
            return True  # Return True when liquidity pairs are found

        else:
            print(Fore.WHITE + '-' * 50)
            print(Fore.RED + f"\nBAD TOKEN: No liquidity pairs found for: {mint_address}\n")
            return False

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching liquidity data for Solana token address: {mint_address}: {e}")
        return False


# get_solana_token_data('7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr')
# Get the mint address from command-line arguments
if len(sys.argv) < 2:
    print("No mint address provided.")
    sys.exit(1)

mint_address = sys.argv[1]

# Run the function with the given mint address
print("Using token address: ", mint_address)
time.sleep(10)
# get_solana_token_data(mint_address)
liquidity_found = get_solana_token_data(mint_address)

time.sleep(1)
# After generating the CSV, call the JavaScript script
if liquidity_found:
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        js_script_path = os.path.join(script_dir, '2_rug_detector_final.js')
        # Execute the Node.js script with the mint address
        result = subprocess.run(
            # ['node', './2_rug_detector_final.js', mint_address],
            ['node', js_script_path, mint_address],
            capture_output=True,  # Capture output so we can print it
            text=True,  # Decode stdout and stderr as text
            check=True  # Raise an exception if the process fails
        )
        print(result.stdout)  # Print the standard output from the Node.js script
        print('2_rug_detector_final.js executed successfully.')
    except subprocess.CalledProcessError as e:
        print(f"Error executing 2_rug_detector_final.js: {e.stderr}", file=sys.stderr)
else:
    print(f"BAD TOKEN: Skipping 2_rug_detector_final.js execution.")
    # pass


### ADD LOGIC HERE TO BUY NEW TOKEN IF SCORE IS GOOD ###
script_dir = os.path.dirname(os.path.abspath(__file__))
rankings_dir = os.path.join(script_dir, 'rankings')
rankings_file_path = os.path.join(rankings_dir, f"{mint_address}_rank.json")

# Check if the rankings file exists
if os.path.exists(rankings_file_path):
    # Load the rankings data from the JSON file
    with open(rankings_file_path, 'r') as f:
        ranking_data = json.load(f)
    
    # Get the rank value
    rank = ranking_data.get('rank')

    # If rank is 3, 4, or 5, execute the buy_token.py script
    if rank in [3, 4, 5]:
        print(f"Token with mint address {mint_address} has a good rank: {rank}. Proceeding to buy.")
        try:
            # Execute the buy_token.py script with the mint address
            buy_script_path = os.path.join(script_dir, 'buy_token.py')
            subprocess.run(['python', buy_script_path, mint_address], check=True)
            print(f"buy_token.py executed successfully for token: {mint_address}")

            monitor_script_path = os.path.join(script_dir, 'monitor_wallet.py')
            subprocess.run(['python', monitor_script_path, mint_address], check=True)
            print(f"monitor_wallet.py executed successfully for token: {mint_address}")

        except subprocess.CalledProcessError as e:
            print(f"Error executing buy_token.py: {e.stderr}")
    else:
        print(f"Token with mint address {mint_address} has rank: {rank}. No action taken.")
else:
    print(f"Rankings file not found for token {mint_address}. Skipping buy step.")