# Get a List of 'Internal' Transactions By Address

import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('BASESCAN_API_KEY')

# Address to check for internal transactions
address = "0xB70AA19beEa17f76099C3a65c3C947dbB2326c44"

# Define the start and end blocks, pagination settings
startblock = 0
endblock = 2702578
page = 1
offset = 10
sort = "asc"

# BaseScan API endpoint to get the list of internal transactions
url = f"https://api.basescan.org/api?module=account&action=txlistinternal&address={address}&startblock={startblock}&endblock={endblock}&page={page}&offset={offset}&sort={sort}&apikey={api_key}"

# Make the request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    with open('./logs/transactions_internal_raw_output.json', 'w') as f:
        f.write(response.text)
    data = response.json()
    if data['status'] == '1':
        internal_transactions = data['result']
        print(f"Total internal transactions found: {len(internal_transactions)}")
        for txn in internal_transactions:
            print(f"Hash: {txn['hash']}, From: {txn['from']}, To: {txn['to']}, Value: {int(txn['value']) / 10**18} Ether")
    else:
        print(f"Error: {data['message']}")
else:
    print(f"Failed to retrieve internal transactions. HTTP Status Code: {response.status_code}")
