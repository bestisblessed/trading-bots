# Get Ether Balance for Multiple Addresses on Base

import requests
import os
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
api_key = os.getenv('BASESCAN_API_KEY')

# List of Base addresses to check balances for
addresses = [
    "0xB70AA19beEa17f76099C3a65c3C947dbB2326c44",
    "0x4216Ecc89c83369f0657FF57E00280b32C33D1c9"
]

# Join the addresses into a single comma-separated string
address_list = ",".join(addresses)

# BaseScan API endpoint to get the Ether balances
url = f"https://api.basescan.org/api?module=account&action=balancemulti&address={address_list}&tag=latest&apikey={api_key}"

# Make the request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    if data['status'] == '1':
        for account in data['result']:
            address = account['account']
            balance_in_wei = int(account['balance'])
            balance_in_ether = balance_in_wei / 10**18  # Convert Wei to Ether
            print(f"Address: {address}")
            print(f"Balance: {balance_in_ether} Ether")
    else:
        print(f"Error: {data['message']}")
else:
    print(f"Failed to retrieve balances. HTTP Status Code: {response.status_code}")
