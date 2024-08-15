import json
import requests
import pandas as pd
from dotenv import load_dotenv
import os
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('BASESCAN_API_KEY')

# BaseScan and Dexscreener API endpoints and parameters
basescan_api_endpoint = 'https://api.basescan.org/api'
dexscreener_api_endpoint = 'https://api.dexscreener.com/latest/dex/tokens'

# Request parameters for BaseScan API
params = {
    'module': 'account',
    'action': 'txlistinternal',
    'startblock': 0,
    'endblock': 9999999999,
    'sort': 'desc',
    'apikey': api_key
}

# Make the API request to fetch internal transactions
response = requests.get(basescan_api_endpoint, params=params)

# Initialize counter for new tokens
new_tokens_count = 0

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    if data['status'] == '1':
        internal_transactions = data['result']
        create_transactions = [tx for tx in internal_transactions if tx['type'] in ['create', 'create2']]
        print(Fore.GREEN + f"Total 'create' or 'create2' transactions: {len(create_transactions)}")

        # Initialize a list to hold all transfer events
        all_transfers = []

        # Fetch token transfer events for each contract address
        for transaction in create_transactions:
            contract_address = transaction['contractAddress']
            if contract_address:
                params = {
                    'module': 'account',
                    'action': 'tokentx',
                    'address': contract_address,
                    'sort': 'asc',
                    'apikey': api_key
                }
                response = requests.get(basescan_api_endpoint, params=params)
                data = response.json()
                if data['status'] == '1':
                    print(Fore.BLUE + f"Transfers for Address: {contract_address}")
                    all_transfers.extend(data['result'])
                else:
                    print(Fore.RED + f"Failed to fetch data for {contract_address}: {data['message']}")

        # Load the transfer events into a DataFrame and find unique tokens
        df = pd.DataFrame(all_transfers)
        unique_tokens = df[['tokenName', 'tokenSymbol', 'contractAddress']].drop_duplicates()

        # Create a dictionary to store liquidity data by token
        liquidity_data = {}

        # Fetch additional data for each unique contract address
        for _, row in unique_tokens.iterrows():
            token_address = row['contractAddress']
            try:
                response = requests.get(f'{dexscreener_api_endpoint}/{token_address}')
                response.raise_for_status()
                token_data = response.json()
                if token_data:
                    if token_data.get('pairs'):
                        for pair in token_data['pairs']:
                            base_token_name = pair['baseToken']['name']
                            base_token_symbol = pair['baseToken']['symbol']
                            base_token_liquidity = pair['liquidity']['base']
                            quote_token_name = pair['quoteToken']['name']
                            quote_token_symbol = pair['quoteToken']['symbol']
                            quote_token_liquidity = pair['liquidity']['quote']
                            usd_liquidity = pair['liquidity']['usd']

                            token_key = f"{base_token_name} ({base_token_symbol})"
                            if token_key not in liquidity_data:
                                liquidity_data[token_key] = {'base': 0, 'quote': 0, 'usd': 0, 'addresses': set()}
                            liquidity_data[token_key]['base'] += base_token_liquidity
                            liquidity_data[token_key]['quote'] += quote_token_liquidity
                            liquidity_data[token_key]['usd'] += usd_liquidity
                            liquidity_data[token_key]['addresses'].add(token_address)
            except requests.exceptions.RequestException as e:
                print(Fore.RED + f'Error fetching token data for {token_address}: {e}')

        print(Fore.YELLOW + "Unique token names, symbols, and liquidity:")
        for _, row in unique_tokens.iterrows():
            token_name = row['tokenName']
            token_symbol = row['tokenSymbol']
            contract_address = row['contractAddress']
            token_key = f"{token_name} ({token_symbol})"
            if token_key in liquidity_data:
                base_liquidity = liquidity_data[token_key]['base']
                quote_liquidity = liquidity_data[token_key]['quote']
                usd_liquidity = liquidity_data[token_key]['usd']
                
                # print(Fore.CYAN + f"{token_name} ({token_symbol}) liquidity: ${usd_liquidity}")
                # print(Fore.CYAN + f"{token_name} ({token_symbol}) liquidity: " + Fore.GREEN + f"${usd_liquidity}")
                print(Fore.CYAN + f"{token_name} ({token_symbol}) " + Fore.GREEN + f"liquidity: ${usd_liquidity}")
                print(Fore.MAGENTA + f"Contract Address: {contract_address}")

                # Save token details to file if it does not already exist
                # token_filename = f"./new_tokens/{token_name}_{token_symbol}.json"
                token_filename = f"./new_tokens/{contract_address}_{token_symbol}.json"
                if not os.path.exists(token_filename):
                    token_info = {
                        'tokenName': token_name,
                        'tokenSymbol': token_symbol,
                        'contractAddress': contract_address,
                        'baseLiquidity': base_liquidity,
                        'quoteLiquidity': quote_liquidity,
                        'usdLiquidity': usd_liquidity
                    }
                    with open(token_filename, 'w') as file:
                        json.dump(token_info, file, indent=4)
                    # print(Fore.GREEN + f"*New*")
                    print(Fore.MAGENTA + f"" + Fore.GREEN + "✨")
                    new_tokens_count += 1
                else:
                    print(Fore.RED + f"Token exists already")

                print(Fore.WHITE + '-' * 50)

        # Print the total number of new tokens saved
        print(Fore.LIGHTRED_EX + f"Total number of new tokens saved: {new_tokens_count}")

    else:
        print(Fore.RED + f"Error: {data['message']}")
else:
    print(Fore.RED + f"Failed to retrieve data. HTTP Status Code: {response.status_code}")








        # # Print unique token names and symbols
        # print(Fore.YELLOW + "Unique token names and symbols:")
        # for _, row in unique_tokens.iterrows():
        #     print(Fore.CYAN + f"{row['tokenName']} (${row['tokenSymbol']} {row['contractAddress']})")

        # # Fetch additional data for each unique contract address
        # additional_data = []
        # for _, row in unique_tokens.iterrows():
        #     token_address = row['contractAddress']
        #     try:
        #         response = requests.get(f'{dexscreener_api_endpoint}/{token_address}')
        #         response.raise_for_status()
        #         token_data = response.json()
        #         if token_data:
        #             additional_data.append(token_data)
        #     except requests.exceptions.RequestException as e:
        #         print(Fore.RED + f'Error fetching token data for {token_address}: {e}')

        # # Extract and print liquidity information
        # liquidity_info = []
        # for item in additional_data:
        #     if item.get('pairs'):
        #         for pair in item['pairs']:
        #             base_token_name = pair['baseToken']['name']
        #             base_token_symbol = pair['baseToken']['symbol']
        #             base_token_liquidity = pair['liquidity']['base']
        #             quote_token_name = pair['quoteToken']['name']
        #             quote_token_symbol = pair['quoteToken']['symbol']
        #             quote_token_liquidity = pair['liquidity']['quote']
        #             usd_liquidity = pair['liquidity']['usd']

        #             liquidity_info.append({
        #                 'base_token_name': base_token_name,
        #                 'base_token_symbol': base_token_symbol,
        #                 'base_token_liquidity': base_token_liquidity,
        #                 'quote_token_name': quote_token_name,
        #                 'quote_token_symbol': quote_token_symbol,
        #                 'quote_token_liquidity': quote_token_liquidity,
        #                 'usd_liquidity': usd_liquidity
        #             })

        # for info in liquidity_info:
        #     if info['base_token_symbol'] != 'WETH':
        #         print(Fore.GREEN + f"{info['base_token_name']} ({info['base_token_symbol']}) liquidity: {info['base_token_liquidity']}")
        #         print(Fore.GREEN + f"{info['quote_token_name']} ({info['quote_token_symbol']}) liquidity: {info['quote_token_liquidity']}")
        #         print(Fore.GREEN + f"USD liquidity: {info['usd_liquidity']}")
        #         print(Fore.GREEN + '-' * 50)


