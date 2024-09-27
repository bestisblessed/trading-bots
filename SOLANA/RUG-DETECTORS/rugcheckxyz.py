import sys
import json
import requests
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the wallet address from the environment variable
wallet_address = os.getenv("MY_BOT_WALLET_ADDRESS")

# Check if the wallet address is loaded
if not wallet_address:
    print("Error: WALLET_ADDRESS not found in the .env file.")
    sys.exit(1)

# Define the path to the token balances file using the wallet address
token_balances_file = f'wallets/{wallet_address}_token_balances.json'

# Load the token balances from the JSON file
with open(token_balances_file, 'r') as f:
    token_balances = json.load(f)

# Check if mint_address argument is provided
if len(sys.argv) < 2:
    # List all token symbols with mint addresses
    print("No mint address provided. Listing all tokens:")
    for token in token_balances:
        print(f"Mint Address: {token['mint']}, Token Symbol: {token['symbol']}, Token Name: {token['name']}")
    sys.exit(0)

# Get the mint address from the command line argument
mint_address = sys.argv[1]

# Find the token symbol for the given mint address
token_info = None
for token in token_balances:
    if token['mint'] == mint_address:
        token_info = token
        symbol = token_info['symbol']
        break

if not token_info:
    print(f"You have none {mint_address} - continuing with rug check.\n")
    symbol = mint_address
    # sys.exit(1)

# url = "https://api.rugcheck.xyz/v1/tokens/21AErpiB8uSb94oQKRcwuHqyHF93njAxBSbdUrpupump/report/summary" # wif
# url = "https://api.rugcheck.xyz/v1/tokens/A8C3xuqscfmyLrte3VmTqrAq8kgMASius9AFNANwpump/report/summary" # fwog
# url = "https://api.rugcheck.xyz/v1/tokens/ezk3nwHdpohYwukZiMCWgwEqqsnfBM7WL1xdmZ9pump/report/summary" # bleh
# url = "https://api.rugcheck.xyz/v1/tokens/CFnREV96uczzbDGqvd8Fhhp9SPSkamy7Xwwk96xHZWjc/report/summary" # mcoin
url = f"https://api.rugcheck.xyz/v1/tokens/{mint_address}/report/summary" # mcoin
response = requests.get(url, headers={"accept": "application/json"})
if response.status_code == 200:
    rug_check_data = response.json()  # Get the JSON response
    # Print the token symbol and rug check report
    print(f"Token Symbol: {symbol}")
    print("Rug Check Report:")
    # print(rug_check_data)  # Print the JSON response
    print(json.dumps(rug_check_data, indent=4))  # Pretty-print the JSON response
    # Assign the last 'score' to final_score variable
    final_score = rug_check_data.get('score', 0)  # Use .get to safely access the score
    print(f"Final Score: {final_score}")

    # If the token is found, add final_score to the token's entry
    if token_info:
        token_info['rugcheckxyz_1'] = final_score

        # Save the updated token balances back to the JSON file
        with open(token_balances_file, 'w') as f:
            json.dump(token_balances, f, indent=2)
            print(f"Added rugcheckxyz score to {token_balances_file}")

else:
    print(f"Error: {response.status_code}")

# Print a message if no updates were saved
if not token_info:
    print("\nNo updates were saved because the token was not found in the balances file.")