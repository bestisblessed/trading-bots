import json
import requests
import pandas as pd
from dotenv import load_dotenv
import os

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

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    if data['status'] == '1':
        internal_transactions = data['result']
        create_transactions = [tx for tx in internal_transactions if tx['type'] in ['create', 'create2']]
        print(f"Total 'create' or 'create2' transactions: {len(create_transactions)}")

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
                    print(f"Transfers for Address: {contract_address}")
                    all_transfers.extend(data['result'])
                else:
                    print(f"Failed to fetch data for {contract_address}: {data['message']}")

        # Load the transfer events into a DataFrame and find unique tokens
        df = pd.DataFrame(all_transfers)
        unique_tokens = df[['tokenName', 'tokenSymbol', 'contractAddress']].drop_duplicates()

        # Print unique token names and symbols
        print("Unique token names and symbols:")
        for _, row in unique_tokens.iterrows():
            print(f"{row['tokenName']} (${row['tokenSymbol']} {row['contractAddress']})")

        # Fetch additional data for each unique contract address
        additional_data = []
        for _, row in unique_tokens.iterrows():
            token_address = row['contractAddress']
            try:
                response = requests.get(f'{dexscreener_api_endpoint}/{token_address}')
                response.raise_for_status()
                token_data = response.json()
                if token_data:
                    additional_data.append(token_data)
            except requests.exceptions.RequestException as e:
                print(f'Error fetching token data for {token_address}: {e}')

        # Extract and print liquidity information
        liquidity_info = []
        for item in additional_data:
            if item.get('pairs'):
                for pair in item['pairs']:
                    base_token_name = pair['baseToken']['name']
                    base_token_symbol = pair['baseToken']['symbol']
                    base_token_liquidity = pair['liquidity']['base']
                    quote_token_name = pair['quoteToken']['name']
                    quote_token_symbol = pair['quoteToken']['symbol']
                    quote_token_liquidity = pair['liquidity']['quote']
                    usd_liquidity = pair['liquidity']['usd']

                    liquidity_info.append({
                        'base_token_name': base_token_name,
                        'base_token_symbol': base_token_symbol,
                        'base_token_liquidity': base_token_liquidity,
                        'quote_token_name': quote_token_name,
                        'quote_token_symbol': quote_token_symbol,
                        'quote_token_liquidity': quote_token_liquidity,
                        'usd_liquidity': usd_liquidity
                    })

        for info in liquidity_info:
            if info['base_token_symbol'] != 'WETH':
                print(f"{info['base_token_name']} ({info['base_token_symbol']}) liquidity: {info['base_token_liquidity']}")
                print(f"{info['quote_token_name']} ({info['quote_token_symbol']}) liquidity: {info['quote_token_liquidity']}")
                print(f"USD liquidity: {info['usd_liquidity']}")
                print('-' * 50)
                
    else:
        print(f"Error: {data['message']}")
else:
    print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")
