import os
import json
import requests
import datetime
from dotenv import load_dotenv
from moralis import sol_api
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Load environment variables from the .env file
load_dotenv()

# Get the API key and wallet address from the environment variables
api_key = os.getenv("MORALIS_API_KEY")
wallet_address = os.getenv("MY_BOT_WALLET_ADDRESS")

# Check if the wallet address was loaded correctly
if not wallet_address:
    print(Fore.RED + "Error: MY_BOT_WALLET_ADDRESS is not set in the .env file")
    exit(1)

# Define the parameters with the Solana wallet address and network
params = {
    "address": wallet_address,  # Get wallet address from .env
    "network": "mainnet",
}
# # Initialize colorama
# init(autoreset=True)

# # Load environment variables from the .env file
# load_dotenv()

# # Get the API key from the environment variables
# api_key = os.getenv("MORALIS_API_KEY")

# # Define the parameters with the Solana wallet address and network
# params = {
#     "address": "7Qq8RTV2ZP3niS1xmrvDf5PemARSJamWk3gVbECP3yaE",
#     "network": "mainnet",
# }

# Fetch the portfolio balance
result = sol_api.account.get_portfolio(api_key=api_key, params=params)

# Extract token balances
tokens = result.get('tokens', [])

# Ensure the data/ directory exists
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Define the path for the output file
wallet_address = params['address']
output_path = os.path.join(data_dir, f'{wallet_address}_token_balances.json')
buy_prices_path = os.path.join(data_dir, 'buy_prices.json')

# Save the current token balances to a JSON file
with open(output_path, 'w') as f:
    json.dump(tokens, f, indent=2)
print(f'Current token balances saved to {output_path}')

# Load existing buy prices (if they exist)
if os.path.exists(buy_prices_path):
    with open(buy_prices_path, 'r') as f:
        buy_prices = json.load(f)
else:
    buy_prices = {}

# Dexscreener API endpoint for Solana tokens
dexscreener_api_endpoint = 'https://api.dexscreener.com/latest/dex/tokens'

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

def get_solana_token_data(token_address):
    # Check if the token is in the blacklist
    if token_address in blacklisted_mint_addresses:
        # print(Fore.RED + f"Token {token_address} is blacklisted. Skipping.")
        return

    if token_address.startswith("So1"):
        print(Fore.RED + f"Skipping token with address starting with 'So1': {token_address}")
        return
    
    try:
        # Make API request to Dexscreener for the Solana token address
        response = requests.get(f'{dexscreener_api_endpoint}/{token_address}')
        response.raise_for_status()  # Raise an exception for HTTP errors
        token_data = response.json()

        # Generate a timestamp for when the data is fetched
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Check if token data and pairs exist and are not None
        if token_data and 'pairs' in token_data and token_data['pairs']:
            print(Fore.WHITE + '-' * 50)
            print(Fore.CYAN + f"  TOKEN ADDRESS: {token_address}")  # Print token address
            
            # Get the first pair only
            pair = token_data['pairs'][0]
            solana_token_name = pair['baseToken']['name']
            solana_token_symbol = pair['baseToken']['symbol']
            solana_token_liquidity = pair.get('liquidity', {}).get('base', 'Liquidity not available')
            quote_token_name = pair['quoteToken']['name']
            quote_token_symbol = pair['quoteToken']['symbol']
            quote_token_liquidity = pair.get('liquidity', {}).get('quote', 'Liquidity not available')
            usd_liquidity = pair.get('liquidity', {}).get('usd', 'USD liquidity not available')
            price_usd = pair.get('priceUsd', 'Price not available')  # Get token price in USD

            # Check if the token is already in buy_prices.json
            if token_address not in buy_prices:
                # Save token details to the buy_prices.json file
                buy_prices[token_address] = {
                    "name": solana_token_name,
                    "symbol": solana_token_symbol,
                    "price_usd": price_usd,
                    "liquidity_usd": usd_liquidity,
                    "timestamp": timestamp
                }
                print(Fore.BLACK + f"  Added token details for {solana_token_name} ({solana_token_symbol}) to buy_prices.json")

                # Save the buy prices back to the buy_prices.json file
                with open(buy_prices_path, 'w') as f:
                    json.dump(buy_prices, f, indent=2)

            # Print liquidity and price details
            print(Fore.YELLOW + f"  {solana_token_name} ({solana_token_symbol}) / {quote_token_name} ({quote_token_symbol})")
            print(Fore.GREEN + f"  Price (USD): {price_usd}")
            print(Fore.GREEN + f"  Timestamp: {timestamp}")
            print(Fore.GREEN + f"  Liquidity (Solana Token): {solana_token_liquidity}")
            print(Fore.GREEN + f"  Liquidity (Quote Token): {quote_token_liquidity}")
            print(Fore.GREEN + f"  Liquidity (USD): {usd_liquidity}")
        else:
            print(Fore.WHITE + '-' * 50)
            print(Fore.RED + f"No liq pairs found for: {token_address}")
    
    except requests.exceptions.RequestException as e:
        # print(Fore.RED + f"Error fetching liquidity data for Solana token address: {token_address}: {e}")
        pass

# Load the token addresses from the previously saved JSON file and check their prices and liquidity
if os.path.exists(output_path):
    with open(output_path, 'r') as f:
        token_data = json.load(f)
        for token in token_data:
            mint_address = token.get('mint')
            if mint_address:
                get_solana_token_data(mint_address)
