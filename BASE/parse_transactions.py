# How to Use These Method IDs:
# Decode Transaction Data:

# You can identify these function calls by decoding the transaction's input data. The first 4 bytes will match one of the Method IDs above, indicating whether the transaction is a buy or sell.
# Analyze Parameters:

# After identifying the method, you can further decode the parameters to determine the exact tokens and amounts being traded.
# Example:
# A transaction with an input data starting with 0x18cbafe5 is likely a sell transaction (selling tokens for ETH).
# A transaction with an input data starting with 0x7ff36ab5 is likely a buy transaction (buying tokens with ETH). 

# Practical Implementation:
# When analyzing transactions on Base, you would:

# Fetch the transaction data using the eth_getTransactionByHash endpoint.
# Extract the first 4 bytes of the input field.
# Compare it to known Method IDs to determine if it's a buy or sell transaction.
# Optionally, decode the rest of the input data to get more details about the transaction.

import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key = os.getenv('BASESCAN_API_KEY')

with open('./logs/logs_by_address.json', 'r') as f:
    logs = json.load(f)

base_url = "https://api.basescan.org/api"

# Function to get transaction details by hash
def get_transaction_details(txhash):
    url = f"{base_url}?module=proxy&action=eth_getTransactionByHash&txhash={txhash}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Successfully fetched details for {txhash}")
        return response.json()
    else:
        print(f"Failed to fetch transaction details for {txhash}")
        return None

# Limit to the first 20 logs
logs_to_process = logs[:1000]

# Iterate through each log and get the transaction details
transaction_details = []
for log in logs_to_process:  # Change logs_to_process to logs to process all entries
    txhash = log['transactionHash']
    details = get_transaction_details(txhash)
    if details:
        transaction_details.append(details)

# Save the transaction details to a file
with open('transaction_details.json', 'w') as f:
    json.dump(transaction_details, f, indent=4)

print("Transaction details have been saved to transaction_details.json")

# Known DEX router addresses on Base chain
dex_router_addresses = {
    "Uniswap V3 Router": "0x2626664c2603336E57B271c5C0b26F421741e481",
    "BaseSwap Router": "0x16e71b13fE6079B4312063F7E81F76d165Ad32Ad"
}

# Load the transaction details from the JSON file
with open('transaction_details.json', 'r') as f:
    transactions = json.load(f)

# Initialize a counter for DEX interactions
dex_interaction_count = 0

# Function to check if a transaction involves a DEX
def check_transaction_for_dex(transaction, dex_addresses):
    global dex_interaction_count
    try:
        result = transaction.get('result', {})
        to_address = result.get('to', '').lower()
        from_address = result.get('from', '').lower()
        
        for dex_name, dex_address in dex_addresses.items():
            if to_address == dex_address.lower() or from_address == dex_address.lower():
                print(f"Transaction {result.get('hash', 'N/A')} interacts with {dex_name}.")
                dex_interaction_count += 1
                break  # No need to check other DEXes if one match is found
    except AttributeError as e:
        print(f"Error processing transaction: {transaction}. Error: {e}")

# Iterate through each transaction and check for DEX interactions
for tx in transactions:
    check_transaction_for_dex(tx, dex_router_addresses)

# Print the total number of transactions interacting with a DEX
print(f"\nTotal number of transactions interacting with a DEX: {dex_interaction_count}")




# for i, log in enumerate(logs_to_process, start=1):
#     txhash = log['transactionHash']
#     print(f"\nProcessing log {i}/{len(logs_to_process)} with transaction hash: {txhash}")
#     details = get_transaction_details(txhash)
    
#     if details:
#         # Extract the first 4 bytes of the input data to identify the function call
#         input_data = details['result']['input']
#         method_id = input_data[:10]  # First 4 bytes + 0x (so 10 characters)
#         print(f"Method ID: {method_id}")

#         # Determine if it's a buy or sell based on the method ID
#         if method_id == '0x7ff36ab5':
#             print("This transaction is likely a buy transaction (buying tokens with ETH).")
#         elif method_id == '0x18cbafe5':
#             print("This transaction is likely a sell transaction (selling tokens for ETH).")
#         else:
#             print("Unknown method ID, could not determine if it's a buy or sell.")

#         transaction_details.append(details)

# # Save the transaction details to a file
# output_file = 'transaction_details_first_10.json'
# with open(output_file, 'w') as f:
#     json.dump(transaction_details, f, indent=4)

# print(f"\nTransaction details have been saved to {output_file}")




# v2
# transaction_details = []
# for i, log in enumerate(logs_to_process, start=1):
#     txhash = log['transactionHash']
#     print(f"\nProcessing log {i}/{len(logs_to_process)} with transaction hash: {txhash}")
#     details = get_transaction_details(txhash)
    
#     if details:
#         # Extract the first 4 bytes of the input data to identify the function call
#         input_data = details['result']['input']
#         method_id = input_data[:10]  # First 4 bytes + 0x (so 10 characters)
#         print(f"Method ID: {method_id}")

#         # Determine if it's a buy or sell based on the method ID
#         if method_id == '0x7ff36ab5':
#             print("This transaction is likely a buy transaction (buying tokens with ETH).")
#         elif method_id == '0x18cbafe5':
#             print("This transaction is likely a sell transaction (selling tokens for ETH).")
#         else:
#             print("Unknown method ID, could not determine if it's a buy or sell.")
