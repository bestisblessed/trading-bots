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

def get_logs_by_topics(from_block, to_block, topic0, topic1, output_file):
    """
    Retrieves event logs by topics and saves them to a file.
    
    Parameters:
    - from_block: The block number to start searching from.
    - to_block: The block number to stop searching at.
    - topic0: The first topic to filter logs by (event signature).
    - topic1: The second topic to filter logs by (e.g., indexed address).
    - output_file: The file to save the raw logs.
    """

    # BaseScan API endpoint for logs by topics
    url = f"https://api.basescan.org/api?module=logs&action=getLogs&fromBlock={from_block}&toBlock={to_block}&topic0={topic0}&topic0_1_opr=and&topic1={topic1}&apikey={api_key}"

    # Make the request to the BaseScan API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data['status'] == '1':
            # Save the raw logs to a file
            with open(output_file, 'w') as f:
                json.dump(data['result'], f, indent=4)
            print(f"Logs by topics saved to {output_file}")
        else:
            print(f"Error (Topics): {data['message']}")
    else:
        print(f"Failed to retrieve logs by topics: {response.status_code}")

# Example usage
get_logs_by_topics(
    from_block=from_block,
    to_block=to_block,
    topic0='0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef',  # Example topic
    topic1='0x0000000000000000000000000000000000000000000000000000000000000000',  # Example topic
    output_file='./logs/logs_by_topics.json'
)
