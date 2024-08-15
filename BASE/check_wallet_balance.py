# Get Ether Balance for a Single Address on Base

import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('BASESCAN_API_KEY')

# Base address to check balance for
address = "0xB70AA19beEa17f76099C3a65c3C947dbB2326c44"

# BaseScan API endpoint to get the Ether balance
url = f"https://api.basescan.org/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}"

# Make the request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    if data['status'] == '1':
        balance_in_wei = int(data['result'])
        balance_in_ether = balance_in_wei / 10**18  # Convert Wei to Ether
        print(f"Address: {address}")
        print(f"Balance: {balance_in_ether} Ether")
    else:
        print(f"Error: {data['message']}")
else:
    print(f"Failed to retrieve balance. HTTP Status Code: {response.status_code}")

