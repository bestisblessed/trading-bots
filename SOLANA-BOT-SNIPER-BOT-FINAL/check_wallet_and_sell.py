# import os
# import json
# import requests
# import datetime
# from dotenv import load_dotenv
# from colorama import init, Fore, Style
# import subprocess  # To run sell_token.py and sell_token_500.py
# from decimal import Decimal  # Use Decimal for high precision

# # Initialize colorama
# init(autoreset=True)

# # Load environment variables from the .env file
# load_dotenv()

# # Get the wallet address from the environment variables
# wallet_address = os.getenv("MY_BOT_WALLET_ADDRESS")

# # Check if the wallet address was loaded correctly
# if not wallet_address:
#     print(Fore.RED + "Error: MY_BOT_WALLET_ADDRESS is not set in the .env file")
#     exit(1)

# # Ensure the data/ directory exists
# data_dir = 'data'
# if not os.path.exists(data_dir):
#     os.makedirs(data_dir)

# # Define the path for the output file (token balances JSON)
# # wallet_address = "7Qq8RTV2ZP3niS1xmrvDf5PemARSJamWk3gVbECP3yaE"  # Example wallet address
# output_path = os.path.join(data_dir, f'{wallet_address}_token_balances.json')
# buy_prices_path = os.path.join(data_dir, 'buy_prices.json')  # Path to your buy prices JSON
# sold_tokens_path = os.path.join(data_dir, 'sold_tokens.json')  # Path to track sold tokens

# # Dexscreener API endpoint for Solana tokens
# dexscreener_api_endpoint = 'https://api.dexscreener.com/latest/dex/tokens'

# # Load the sold tokens if it exists, else create an empty dictionary
# if os.path.exists(sold_tokens_path):
#     with open(sold_tokens_path, 'r') as f:
#         sold_tokens = json.load(f)
# else:
#     sold_tokens = {}

# # print(" ")

# def get_solana_token_data(token_address, buy_price_usd):
#     if token_address.startswith("So1"):
#         print(Fore.RED + f"Skipping token with address starting with 'So1': {token_address}")
#         return
    
#     try:
#         # Make API request to Dexscreener for the Solana token address
#         response = requests.get(f'{dexscreener_api_endpoint}/{token_address}')
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         token_data = response.json()

#         # Generate a timestamp for when the data is fetched
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

#         # Check if token data and pairs exist and are not None
#         if token_data and 'pairs' in token_data and token_data['pairs']:
#             # print(Fore.WHITE + '-' * 50)
#             # print(Fore.CYAN + f"\n  TOKEN ADDRESS: {token_address}")  # Print token address
            
#             # Get the first pair only
#             pair = token_data['pairs'][0]
#             # price_usd = float(pair.get('priceUsd', '0'))  # Get token price in USD
#             price_usd = Decimal(pair.get('priceUsd', '0'))  # Use Decimal for high precision
#             buy_price_usd = Decimal(buy_price_usd)

#             # Calculate price increase
#             if buy_price_usd > 0:
#                 price_increase_percentage = ((price_usd - buy_price_usd) / buy_price_usd) * 100
                

#                 # Check if price has increased by 500% or more
#                 if price_increase_percentage >= 500:
#                     print(Fore.GREEN + f"Price increased by {price_increase_percentage:.2f}%! Triggering sell for 500% increase: {token_address}.")
#                     # Run the sell_token_500.py script
#                     subprocess.run(['python', 'sell_token_500.py', token_address])

#                 # Check if token has already been sold for 50% or 500% increase
#                 if token_address in sold_tokens:
#                     # print(Fore.GREEN + f"Token {token_address} has already been sold at 50% gain, skipping.")
#                     # print(Fore.WHITE + '-' * 50)
#                     return

#                 # Check if price has increased by 50% or more
#                 elif price_increase_percentage >= 50:
#                     print(Fore.GREEN + f"Price increased by {price_increase_percentage:.2f}%! Triggering sell for 50% increase: {token_address}.")
#                     # Run the sell_token.py script
#                     subprocess.run(['python', 'sell_token_100.py', token_address])
#                     sold_tokens[token_address] = {'sell_percentage': 50, 'timestamp': timestamp}  # Add to sold tokens
#                     save_sold_tokens()  # Save the file here after 500% sale

#                 else:
#                     # print(Fore.MAGENTA + f"Price increase is only {price_increase_percentage:.2f}%, not triggering a sell.")
#                     # print(Fore.WHITE + '-' * 50)
#                     pass

#             else:
#                 print(Fore.RED + f"Invalid buy price for {token_address}.")
    
#     except requests.exceptions.RequestException as e:
#         print(Fore.RED + f"Error fetching liquidity data for Solana token address: {token_address}: {e}")

# # Save sold tokens to the sold_tokens.json file
# def save_sold_tokens():
#     with open(sold_tokens_path, 'w') as f:
#         json.dump(sold_tokens, f, indent=4)

# # Load buy prices from buy_prices.json
# if os.path.exists(buy_prices_path):
#     with open(buy_prices_path, 'r') as f:
#         buy_prices = json.load(f)
# else:
#     print(Fore.RED + f"Buy prices file not found: {buy_prices_path}")
#     buy_prices = {}

# # Load the token mint addresses from the previously saved JSON file
# if os.path.exists(output_path):
#     with open(output_path, 'r') as f:
#         token_data = json.load(f)
        
#         # Check if token_data is a list (as in your JSON structure)
#         if isinstance(token_data, list):
#             for token in token_data:
#                 token_address = token.get('mint')
#                 token_symbol = token.get('symbol')  # Extract the symbol for each token
#                 # if token_symbol:
#                     # print(Fore.YELLOW + f"Token Symbol: {token_symbol}")

#                 # Check if we have the buy price for the token
#                 if token_address and token_address in buy_prices:
#                     buy_price_usd = float(buy_prices[token_address].get('price_usd', '0'))
#                     # print(Fore.CYAN + f"Fetching data for token mint address: {token_address}")
#                     get_solana_token_data(token_address, buy_price_usd)
#                 else:
#                     print(Fore.RED + f"No buy price found for token address: {token_address}")
#         else:
#             print(Fore.RED + "Unexpected format in the JSON file. Expected a list.")
# else:
#     print(Fore.RED + f"File not found: {output_path}")
import os
import json
import requests
import datetime
from dotenv import load_dotenv
from colorama import init, Fore, Style
import subprocess  # To run sell_token.py and sell_token_500.py
from decimal import Decimal  # Use Decimal for high precision

# Initialize colorama
init(autoreset=True)

# Load environment variables from the .env file
load_dotenv()

# Get the wallet address from the environment variables
wallet_address = os.getenv("MY_BOT_WALLET_ADDRESS")

# Check if the wallet address was loaded correctly
if not wallet_address:
    print(Fore.RED + "Error: MY_BOT_WALLET_ADDRESS is not set in the .env file")
    exit(1)

# Ensure the data/ directory exists
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Define the path for the output file (token balances JSON)
output_path = os.path.join(data_dir, f'{wallet_address}_token_balances.json')
buy_prices_path = os.path.join(data_dir, 'buy_prices.json')  # Path to your buy prices JSON
sold_tokens_path = os.path.join(data_dir, 'sold_tokens.json')  # Path to track sold tokens

# Dexscreener API endpoint for Solana tokens
dexscreener_api_endpoint = 'https://api.dexscreener.com/latest/dex/tokens'

# Load the sold tokens if it exists, else create an empty dictionary
if os.path.exists(sold_tokens_path):
    with open(sold_tokens_path, 'r') as f:
        sold_tokens = json.load(f)
else:
    sold_tokens = {}


# Define a blacklist of token mint addresses
blacklisted_mint_addresses = [
    "Ft379JgZeZiUpdgeZ2at1vrua6BRZ4zSxAzJA97pump",  # Smol Silly Cat
    "AC2rXHST3J15pQjC9egQM1NG9nAJFdJs5UY7juKnpump",  # Attack cat
    "AceZsMCrm9Ft3faC7HEwQhtZ17W28yhtSMj1iWdvA8DJ",  # NVIDIA
    "F27fm4svbg3WF4bD8HQ412EmGDyVD9gTGRAv3HDtpjKX",  # Steph Curry
    "Geby8f8AcVguhKk2HWbH7vQNAEjHSfmYDxqb3YeNpump",  # Tsuki
    "5vm2Q2H7jXGGZNUMeSFcZHK6xDBPiqAUGicPnrLgpump",  # fire pussy
    "8yTPx3vvxyu99vawVNLFKZnZeFCTZbNHjqdmUTVbpump",  # ant
    "GhFYGUVc74iDSNcy6jz1sjM2GKBaxxdyrLxN4upd8o3E",  # FIRSTFWOG
    "DMy7gxcGFJcPSwGyVm2VdwieP3BwpZTnKQmbZ93Gpump",  # Mr Paca
    "6N26TiQmQ52hMnRMs6FFYLLuE9SEnkgofhZfD9dvpump",  # ali
    "DTDh5a5jxZWteKAT1NFM5QXAPuWk15oFruEgw9pVWGzf",  # Dinoh Coin
    "Z6akXpS92DH5FWFHVU6YYGLJd2XaPo1vZdyF6JDpump",  # Tron
    "7QtA5Bg4eLtVbD7X7oDohxuRqzN9mRkuFoXKpoHdhQ1h",  # Grass
    "rk54dG96SND7Y5V54ugm1X2WzxKZhrkczeZ1uEZpump",  # OUR Solana
    "2WqFfneMQQuSnFeNZPiqi5r5jJTHFUYQ9hUCSjZipump",  # Sand Dog
    "C1YhxP4gnnGnbGAe3VhxdQV4LGqmsXxFFb2HHL3tpump",  # SEAN KINGSTON
    "Dx9xH9ACdX4yQWBkMEKz6uQ6yBioAUgLm2jBHy8Bpump",  # ashaley
    "sHHdByEeznidqFvCj75iPK5uRD9SivNapD1rXLptBP4",   # Naruto
    "M49wideShuYwmnBMi3xXBoGnfg2TpTYAWyLt9QApump",   # Snapcat
    "HidqA4SP1owM2FXGBuypJZxqr8VgoGkcXVZvEr6FZFgy",  # Blobby
    "3M2vepByfZTG6xUSmFidvSCFzHWFoVw7cPvyRDnUpump",  # KOLT
    "CVUo3fiJDxHXtfGtS4eND3WKRMr54Lwfw4cd2Pnipump",  # discord cat
    "NJbXipySpPwnsE72kiBJ6X8S5Whyk4mWyMrbJg9PqkQ",  # YEAH
    "8XLq5abJUb3rhvbExaQAnXUGmXje7Po55bA6VJ5Npump",  # Mr Paca
    "91d14ov7igkGaHoHxKHT2u7TRyLtCih93DeFPUDspump",  # trashKitty
    "4qkLHhLqrzeJCkC61XF82F4FieUzrqX6nzzEWG7rjPNC",  # Make America Wealthy Again
    "5xmnJLPMAgHSpLDR5GMuBWokw7yNdBCHBsV8ooAxpump",  # nono
    "ApdjMxu7xcLTajTxrivmHaJDVLPYaeTeBeUQmz4qpump",  # Puffy
    "EeK6Xd7jAUxjwURzvhV1vWpLHGX1JP6QbahBwATG8Qno",  # NVIDIA
    "6XMXfMFX8S3gU21YThyf6hkifNM61ejRKvuvu8jApump",  # PIPICAT
    "6LRHCKvqCX9JuQj8Fkx8yEM3c1PpyrV9NuPujc9Qpump",  # abcde
    "5WVEKZRXxdTUWnv2ifNCfoKgQR2LfXpoKQDLMfZBpump",  # Trump X
    "BdQUTM2gZnx6kMtidWncw5MPvnv1RNiofHFSSpezKwep",  # Soly The Mascot
    "cLAaRTYScomqVpcf5a3ftFoSAU8sBMnELfo5qwHcYTq",   # WALLAHI IM FINISHED
    "3Z9o7qc5Cq5B9LWecxvgLoJTtrpCmv3fhbZArbnxwVTh",  # Blasted Cat
    "GSomyV7ZxYnKpDzfeWxUSeq3REqMDNMfXvt3ou83pump",  # Grumpy Sam
    "H7UBVmK2jKiedfkUcC8JiAzh6yDsvmV5Ev8oU8S6Z4Qy",  # Red Trump
    "2mnGSkXH1h6x5qmhwoQzAZDKa83vnRf8wNkNWVbdv7w5",  # Strudels on Solana
    "AxoZRsp5NV8DsufRxtMzuAGYseCVPre3RsTMrkzmnwpR",  # APO
    "B4gtR5n7BEMeyWmJfPqamdMRvQ8y7xNWeebFg53Apump",  # NILLY
    "9MBzpyMRkj2r5nTQZMMnxnCm5j1MAAFSYUtbSKjAF3WU",  # Zoomer
    "EKEWAk7hfnwfR8DBb1cTayPPambqyC7pwNiYkaYQKQHp",  # Roaring Kitty
]

def get_solana_token_data(token_address, buy_price_usd):
    # Check if the token is in the blacklist
    if token_address in blacklisted_mint_addresses:
        # print(Fore.RED + f"Token {token_address} is blacklisted. Skipping.")
        return

    # Continue to skip tokens starting with 'So1'
    if token_address.startswith("So1"):
        print(Fore.RED + f"Skipping token with address starting with 'So1': {token_address}")
        return
# def get_solana_token_data(token_address, buy_price_usd):
#     if token_address.startswith("So1"):
#         print(Fore.RED + f"Skipping token with address starting with 'So1': {token_address}")
#         return
    
    try:
        # Make API request to Dexscreener for the Solana token address
        response = requests.get(f'{dexscreener_api_endpoint}/{token_address}')
        response.raise_for_status()  # Raise an exception for HTTP errors
        token_data = response.json()

        # Generate a timestamp for when the data is fetched
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        if token_data and 'pairs' in token_data and token_data['pairs']:
            pair = token_data['pairs'][0]
            price_usd = Decimal(pair.get('priceUsd', '0'))  # Use Decimal for high precision
            buy_price_usd = Decimal(buy_price_usd)

            if buy_price_usd > 0:
                price_increase_percentage = ((price_usd - buy_price_usd) / buy_price_usd) * 100

                # Check if the token has already been sold for a 500% increase
                if token_address in sold_tokens and sold_tokens[token_address].get('sell_500_percent', False):
                    # print(Fore.GREEN + f"Token {token_address} has already been sold at 500% gain, skipping.")
                    return

                # Check if price has increased by 500% or more
                if price_increase_percentage >= 500:
                    print(Fore.GREEN + f"Price increased by {price_increase_percentage:.2f}%! Triggering sell for 500% increase: {token_address}")
                    subprocess.run(['python', 'sell_token_500.py', token_address])
                    sold_tokens[token_address] = {
                        'sell_100_percent': sold_tokens.get(token_address, {}).get('sell_100_percent', False),
                        'sell_500_percent': True, 'timestamp': timestamp
                    }
                    save_sold_tokens()  # Save the file after the 500% sale
                    return

                # Check if the token has already been sold for a 100% increase
                if token_address in sold_tokens and sold_tokens[token_address].get('sell_100_percent', False):
                    # print(Fore.GREEN + f"Token {token_address} has already been sold at 100% gain, skipping.")
                    return

                # Check if price has increased by 100% or more
                elif price_increase_percentage >= 100:
                    print(Fore.GREEN + f"Price increased by {price_increase_percentage:.2f}%! Triggering sell for 100% increase: {token_address}")
                    subprocess.run(['python', 'sell_token_100.py', token_address])
                    sold_tokens[token_address] = {
                        'sell_100_percent': True,
                        'sell_500_percent': False, 'timestamp': timestamp
                    }
                    save_sold_tokens()  # Save the file here after 100% sale

                else:
                    # print(Fore.MAGENTA + f"Price increase is only {price_increase_percentage:.2f}%, not triggering a sell.")
                    pass
            else:
                print(Fore.RED + f"Invalid buy price for {token_address}.")

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching liquidity data for Solana token address: {token_address}: {e}")

# Save sold tokens to the sold_tokens.json file
def save_sold_tokens():
    with open(sold_tokens_path, 'w') as f:
        json.dump(sold_tokens, f, indent=4)

# Load buy prices from buy_prices.json
if os.path.exists(buy_prices_path):
    with open(buy_prices_path, 'r') as f:
        buy_prices = json.load(f)
else:
    print(Fore.RED + f"Buy prices file not found: {buy_prices_path}")
    buy_prices = {}

# Load the token mint addresses from the previously saved JSON file
if os.path.exists(output_path):
    with open(output_path, 'r') as f:
        token_data = json.load(f)
        
        # Check if token_data is a list (as in your JSON structure)
        if isinstance(token_data, list):
            for token in token_data:
                token_address = token.get('mint')
                token_symbol = token.get('symbol')  # Extract the symbol for each token

                # Check if we have the buy price for the token
                if token_address and token_address in buy_prices:
                    buy_price_usd = float(buy_prices[token_address].get('price_usd', '0'))
                    get_solana_token_data(token_address, buy_price_usd)
                else:
                    # print(Fore.RED + f"No buy price found for token address: {token_address}")
                    pass
        else:
            print(Fore.RED + "Unexpected format in the JSON file. Expected a list.")
else:
    print(Fore.RED + f"File not found: {output_path}")
