# Get a List of 'Normal' Transactions By Address

import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.getenv('BASESCAN_API_KEY')

# Address to check for transactions
# address = "0xB70AA19beEa17f76099C3a65c3C947dbB2326c44"
address = "0x4216Ecc89c83369f0657FF57E00280b32C33D1c9"

# # Define the start and end blocks, pagination settings
# startblock = 0
# endblock = 99999999
# page = 1
# offset = 10
# sort = "asc"

# # BaseScan API endpoint to get the list of transactions
# url = f"https://api.basescan.org/api?module=account&action=txlist&address={address}&startblock={startblock}&endblock={endblock}&page={page}&offset={offset}&sort={sort}&apikey={api_key}"

# # Make the request
# response = requests.get(url)

# # Check if the request was successful
# if response.status_code == 200:
#     with open('./logs/transactions_raw_output.json', 'w') as f:
#         f.write(response.text)
#     data = response.json()
#     if data['status'] == '1':
#         transactions = data['result']
#         print(f"Total transactions found: {len(transactions)}")
#         for txn in transactions:
#             print(f"Hash: {txn['hash']}, From: {txn['from']}, To: {txn['to']}, Value: {int(txn['value']) / 10**18} Ether")
#     else:
#         print(f"Error: {data['message']}")
# else:
#     print(f"Failed to retrieve transactions. HTTP Status Code: {response.status_code}")
# Define the start and end blocks, and sorting preference
startblock = 0
endblock = 99999999
sort = "asc"

# Pagination settings
page = 1
offset = 100  # Adjust this to a larger number if you want to fetch more transactions per request

# Container for all transactions
all_transactions = []

while True:
    # Construct the API request URL
    url = f"https://api.basescan.org/api?module=account&action=txlist&address={address}&startblock={startblock}&endblock={endblock}&page={page}&offset={offset}&sort={sort}&apikey={api_key}"
    
    # Make the request
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data['status'] == '1':
            transactions = data['result']
            all_transactions.extend(transactions)  # Add to the list of all transactions
            print(f"Fetched {len(transactions)} transactions on page {page}.")
            
            # Break the loop if there are no more transactions to fetch
            if len(transactions) < offset:
                break
            else:
                page += 1  # Increment the page number to fetch the next set of transactions
        else:
            print(f"Error: {data['message']}")
            break
    else:
        print(f"Failed to retrieve transactions. HTTP Status Code: {response.status_code}")
        break

# Save all transactions to a file
with open('./logs/transactions_raw_output.json', 'w') as f:
    json.dump(all_transactions, f, indent=4)

# Print the total number of transactions found
print(f"Total transactions found: {len(all_transactions)}")

# Optionally print the details of each transaction
for txn in all_transactions:
    print(f"Hash: {txn['hash']}, From: {txn['from']}, To: {txn['to']}, Value: {int(txn['value']) / 10**18} Ether")