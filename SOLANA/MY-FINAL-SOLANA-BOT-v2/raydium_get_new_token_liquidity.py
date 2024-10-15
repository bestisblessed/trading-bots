import requests
import json
import datetime
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

# Raydium API Endpoint
raydium_api_endpoint = 'https://api.raydium.io/v2/main/pairs'

# Function to fetch and print pairs with the given token address
def get_raydium_token_data(token_address):
    try:
        # Make the API request to fetch the token pairs from Raydium
        response = requests.get(raydium_api_endpoint)
        response.raise_for_status()  # Raise exception if the request fails
        pairs_data = response.json()

        # Debugging: Print the number of pairs returned
        print(Fore.CYAN + f"Total pairs fetched: {len(pairs_data)}")

        # Flag to indicate if token was found
        found = False

        # Print only the pairs that match the given token address
        for pair in pairs_data:
            if token_address in (pair['baseMint'], pair['quoteMint']):
            # if token_address in (pair['baseMint']):
                found = True
                print(json.dumps(pair, indent=4))  # Print the entire matching pair in JSON format

        if not found:
            print(Fore.RED + f"Token address {token_address} not found in the pairs.")

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching Raydium data for {token_address}: {e}")


# Example usage
token_address = 'Csr24afRg9jZnLA4m2VcgdWsEiSewsjXmaZ8zbcLpump'
# token_address = '7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr'
get_raydium_token_data(token_address)
