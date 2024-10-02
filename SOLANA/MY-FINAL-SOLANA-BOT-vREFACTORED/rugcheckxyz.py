import sys
import json
import requests
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
# load_dotenv()

# Get the absolute path to the .env file
env_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.env'))

# Load environment variables from the .env file
load_dotenv(env_file_path)

# Get the wallet address from the environment variable
wallet_address = os.getenv("MY_BOT_WALLET_ADDRESS")

# Get the absolute path of the current directory
base_dir = os.path.abspath(os.getcwd())

# Define the path to the rankings directory using the absolute path
rankings_dir = os.path.join(base_dir, 'rankings')
wallets_dir = os.path.join(base_dir, 'wallets')

# Check if the wallet address is loaded
if not wallet_address:
    print("Error: WALLET_ADDRESS not found in the .env file.")
    sys.exit(1)

# Define the path to the token balances file using the wallet address
# token_balances_file = f'wallets/{wallet_address}_token_balances.json'
token_balances_file = os.path.join(wallets_dir, f'{wallet_address}_token_balances.json')

# Load the token balances from the JSON file
with open(token_balances_file, 'r') as f:
    token_balances = json.load(f)

# Check if mint_address argument is provided
if len(sys.argv) < 2:
    # List all token symbols with mint addresses
    # print("No mint address provided. Run >python rugcheckxyz.py <mint_address>")
    print("No mint address provided. Listing all tokens:")
    for token in token_balances:
        print(f"Mint Address: {token['mint']}, Token Symbol: {token['symbol']}, Token Name: {token['name']}")
    sys.exit(0)

# Get the mint address from the command line argument
mint_address = sys.argv[1]

# Define the path to the rankings file using the mint address
# rankings_file = f'rankings/{mint_address}_rank.json'
rankings_file = os.path.join(rankings_dir, f'{mint_address}_rank.json')


# Check if the rankings file exists
if not os.path.exists(rankings_file):
    print(f"Rankings file not found for mint address: {mint_address}")
    sys.exit(1)

# Load the rankings file
with open(rankings_file, 'r') as f:
    ranking_data = json.load(f)

# # Find the token symbol for the given mint address
# token_info = None
# for token in token_balances:
#     if token['mint'] == mint_address:
#         token_info = token
#         symbol = token_info['symbol']
#         break

# if not token_info:
#     print(f"You have none {mint_address} - continuing with rug check.\n")
#     symbol = mint_address
#     # sys.exit(1)

# url = "https://api.rugcheck.xyz/v1/tokens/21AErpiB8uSb94oQKRcwuHqyHF93njAxBSbdUrpupump/report/summary" # wif
# url = "https://api.rugcheck.xyz/v1/tokens/A8C3xuqscfmyLrte3VmTqrAq8kgMASius9AFNANwpump/report/summary" # fwog
# url = "https://api.rugcheck.xyz/v1/tokens/ezk3nwHdpohYwukZiMCWgwEqqsnfBM7WL1xdmZ9pump/report/summary" # bleh
# url = "https://api.rugcheck.xyz/v1/tokens/CFnREV96uczzbDGqvd8Fhhp9SPSkamy7Xwwk96xHZWjc/report/summary" # mcoin
url = f"https://api.rugcheck.xyz/v1/tokens/{mint_address}/report/summary" # mcoin
response = requests.get(url, headers={"accept": "application/json"})
# if response.status_code == 200:
#     rug_check_data = response.json()  # Get the JSON response
#     # Print the token symbol and rug check report
#     print(f"Token Symbol: {symbol}")
#     print("Rug Check Report:")
#     # print(rug_check_data)  # Print the JSON response
#     print(json.dumps(rug_check_data, indent=4))  # Pretty-print the JSON response
#     # Assign the last 'score' to final_score variable
#     final_score = rug_check_data.get('score', 0)  # Use .get to safely access the score
#     print(f"Final Score: {final_score}")

#     # If the token is found, add final_score to the token's entry
#     if token_info:
#         token_info['rugcheckxyz_1'] = final_score

#         # Save the updated token balances back to the JSON file
#         with open(token_balances_file, 'w') as f:
#             json.dump(token_balances, f, indent=2)
#             print(f"Added rugcheckxyz score to {token_balances_file}")

# else:
#     print(f"Error: {response.status_code}")

# # Print a message if no updates were saved
# if not token_info:
#     print("\nNo updates were saved because the token was not found in the balances file.")
if response.status_code == 200:
    rug_check_data = response.json()
    print(f"Rug Check Report for {mint_address}:")
    print(json.dumps(rug_check_data, indent=4))  # Pretty-print the JSON response

    # Get the final score from the rug check data
    # final_score = rug_check_data.get('score', 0)
    final_score = 0
    print(f"Final Score: {final_score}")

    # Add or update the 'rugcheck_1' field in the ranking data
    ranking_data['rugcheckxyz_1'] = final_score

    # Save the updated ranking data back to the file
    with open(rankings_file, 'w') as f:
        json.dump(ranking_data, f, indent=2)
        print(f"Added rugcheckxyz_1 score to {rankings_file}")

else:
    print(f"Error: {response.status_code}")