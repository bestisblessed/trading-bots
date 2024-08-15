import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key = os.getenv('BASESCAN_API_KEY')

# The contract address from which to retrieve logs
contract_address = '0x9bEec80e62aA257cED8b0edD8692f79EE8783777'

# Block range for the search (replace with your desired range)
from_block = '0'
to_block = '9999999999' 

def get_logs_by_address(contract_address, from_block, to_block, output_file):
    """
    Retrieves event logs by address and saves them to a file.
    
    Parameters:
    - contract_address: The contract address to retrieve logs from.
    - from_block: The block number to start searching from.
    - to_block: The block number to stop searching at.
    - output_file: The file to save the raw logs.
    """

    # BaseScan API endpoint for logs by address
    url = f"https://api.basescan.org/api?module=logs&action=getLogs&address={contract_address}&fromBlock={from_block}&toBlock={to_block}&apikey={api_key}"

    # Make the request to the BaseScan API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data['status'] == '1':
            # Save the raw logs to a file
            with open(output_file, 'w') as f:
                json.dump(data['result'], f, indent=4)
            print(f"Logs by address saved to {output_file}")
        else:
            print(f"Error (Address): {data['message']}")
    else:
        print(f"Failed to retrieve logs by address: {response.status_code}")

# Example usage
get_logs_by_address(
    contract_address=contract_address,
    from_block=from_block,
    to_block=to_block,
    output_file='./logs/logs_by_address.json'
)