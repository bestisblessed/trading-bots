# "functionName": "mint(string _json_url,uint256 _location)",

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

# BaseScan API endpoint and parameters
basescan_api_endpoint = 'https://api.basescan.org/api'

# Define the start and end blocks, pagination settings
startblock = 0
endblock = 99999999
sort = "asc"
page = 1
offset = 100  # Adjust this based on how many transactions you want to fetch per request

# Container for all transactions
all_transactions = []

# Make the API request to fetch normal transactions in a loop to handle pagination
while True:
    # Construct the API request URL for normal transactions
    url = f"{basescan_api_endpoint}?module=account&action=txlist&startblock={startblock}&endblock={endblock}&page={page}&offset={offset}&sort={sort}&apikey={api_key}"
    
    # Make the API request to fetch normal transactions
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data['status'] == '1':
            transactions = data['result']
            all_transactions.extend(transactions)  # Add to the list of all transactions
            print(Fore.GREEN + f"Fetched {len(transactions)} transactions on page {page}.")
            
            # Break the loop if there are no more transactions to fetch
            if len(transactions) < offset:
                print(Fore.YELLOW + "No more transactions to fetch.")
                break
            else:
                page += 1  # Increment the page number to fetch the next set of transactions
        else:
            print(Fore.RED + f"Error: {data['message']}")
            break
    else:
        print(Fore.RED + f"Failed to retrieve transactions. HTTP Status Code: {response.status_code}")
        break

# Save all transactions to a file
with open('./logs/transactions_raw_output.json', 'w') as f:
    json.dump(all_transactions, f, indent=4)

# Print the total number of transactions found
print(Fore.LIGHTCYAN_EX + f"Total transactions found: {len(all_transactions)}")

# Process the transactions to find contract creations and other relevant activities
for txn in all_transactions:
    if txn['contractAddress']:
        print(Fore.CYAN + f"Contract created: {txn['contractAddress']} in transaction {txn['hash']}")
    elif txn['methodId'] and txn['functionName']:
        print(Fore.MAGENTA + f"Method ID: {txn['methodId']} | Function: {txn['functionName']} | To: {txn['to']}")

# You can expand this section to analyze specific method IDs, to/from addresses, or other transaction details as needed.
