import requests
from dotenv import load_dotenv
import os
import time

load_dotenv()
api_key = os.getenv('BASESCAN_API_KEY')

# Get the current UNIX timestamp
timestamp = int(time.time())  # Gets the current time in seconds since the Unix epoch

# The 'closest' parameter (either 'before' or 'after')
closest = 'before'  # Choose 'before' or 'after' based on your requirement

# BaseScan API endpoint
url = f"https://api.basescan.org/api?module=block&action=getblocknobytime&timestamp={timestamp}&closest={closest}&apikey={api_key}"

# Make the request to the BaseScan API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    if data['status'] == '1':
        block_number = data['result']
        print(f"The block number closest to the current timestamp {timestamp} ({closest}) is: {block_number}")
    else:
        print(f"Error: {data['message']}")
else:
    print(f"Failed to retrieve data: {response.status_code}")
