# # import requests
# # import json
# # from colorama import init, Fore, Style

# # # Initialize colorama
# # init(autoreset=True)

# # # Dexscreener API endpoint
# # dexscreener_api_endpoint = 'https://api.dexscreener.com/latest/dex/tokens'

# # def get_liquidity_data(token_address):
# #     try:
# #         # Make API request to Dexscreener for the token address
# #         response = requests.get(f'{dexscreener_api_endpoint}/{token_address}')
# #         response.raise_for_status()  # Raise an exception for HTTP errors
# #         token_data = response.json()
        
# #         # Check if token data and pairs exist
# #         if token_data and 'pairs' in token_data:
# #             print(Fore.GREEN + f"Liquidity data for token address: {token_address}")
            
# #             for pair in token_data['pairs']:
# #                 base_token_name = pair['baseToken']['name']
# #                 base_token_symbol = pair['baseToken']['symbol']
# #                 base_token_liquidity = pair['liquidity']['base']
# #                 quote_token_name = pair['quoteToken']['name']
# #                 quote_token_symbol = pair['quoteToken']['symbol']
# #                 quote_token_liquidity = pair['liquidity']['quote']
# #                 usd_liquidity = pair['liquidity']['usd']
# #                 # price_usd = pair.get('priceUsd', 'Price not available')
                
# #                 # Print liquidity details
# #                 print(Fore.CYAN + f"  {base_token_name} ({base_token_symbol})/{quote_token_name} ({quote_token_symbol})")
# #                 print(Fore.GREEN + f"  Liquidity (Base): {base_token_liquidity}")
# #                 print(Fore.GREEN + f"  Liquidity (Quote): {quote_token_liquidity}")
# #                 print(Fore.GREEN + f"  Liquidity (USD): {usd_liquidity}")
# #                 print(Fore.WHITE + '-' * 50)
# #         else:
# #             print(Fore.RED + f"No liquidity pairs found for token address: {token_address}")
    
# #     except requests.exceptions.RequestException as e:
# #         print(Fore.RED + f"Error fetching liquidity data for {token_address}: {e}")

# # # Example: Input a token contract address to fetch its liquidity data
# # token_address = "EbZh3FDVcgnLNbh1ooatcDL1RCRhBgTKirFKNoGPpump"
# # get_liquidity_data(token_address)
# import requests
# import json
# import datetime
# from colorama import init, Fore, Style

# # Initialize colorama
# init(autoreset=True)

# # Dexscreener API endpoint
# dexscreener_api_endpoint = 'https://api.dexscreener.com/latest/dex/tokens'

# def get_liquidity_and_price_data(token_address):
#     try:
#         # Make API request to Dexscreener for the token address
#         response = requests.get(f'{dexscreener_api_endpoint}/{token_address}')
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         token_data = response.json()

#         # Generate a timestamp for when the data is fetched
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

#         # Check if token data and pairs exist
#         if token_data and 'pairs' in token_data:
#             print(Fore.GREEN + f"Liquidity and price data for token address: {token_address}")
            
#             for pair in token_data['pairs']:
#                 solana_token_name = pair['solanaToken']['name']
#                 solana_token_symbol = pair['solanaToken']['symbol']
#                 solana_token_liquidity = pair['liquidity']['solana']
#                 quote_token_name = pair['quoteToken']['name']
#                 quote_token_symbol = pair['quoteToken']['symbol']
#                 quote_token_liquidity = pair['liquidity']['quote']
#                 usd_liquidity = pair['liquidity']['usd']
#                 price_usd = pair.get('priceUsd', 'Price not available')  # Get token price in USD

#                 # Print liquidity and price details
#                 print(Fore.CYAN + f"  {solana_token_name} ({solana_token_symbol})/{quote_token_name} ({quote_token_symbol})")
#                 print(Fore.GREEN + f"  Liquidity (solana): {solana_token_liquidity}")
#                 print(Fore.GREEN + f"  Liquidity (Quote): {quote_token_liquidity}")
#                 print(Fore.GREEN + f"  Liquidity (USD): {usd_liquidity}")
#                 print(Fore.GREEN + f"  Price (USD): {price_usd}")
#                 print(Fore.GREEN + f"  Timestamp: {timestamp}")
#                 print(Fore.WHITE + '-' * 50)
#         else:
#             print(Fore.RED + f"No liquidity pairs found for token address: {token_address}")
    
#     except requests.exceptions.RequestException as e:
#         print(Fore.RED + f"Error fetching liquidity data for {token_address}: {e}")

# # Example: Input a token contract address to fetch its liquidity and price data
# token_address = "EbZh3FDVcgnLNbh1ooatcDL1RCRhBgTKirFKNoGPpump"
# get_liquidity_and_price_data(token_address)
import requests
import json
import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Dexscreener API endpoint for Solana tokens
dexscreener_api_endpoint = 'https://api.dexscreener.com/latest/dex/tokens'

def get_solana_token_data(token_address):
    try:
        # Make API request to Dexscreener for the Solana token address
        response = requests.get(f'{dexscreener_api_endpoint}/{token_address}')
        response.raise_for_status()  # Raise an exception for HTTP errors
        token_data = response.json()

        # Generate a timestamp for when the data is fetched
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Check if token data and pairs exist
        if token_data and 'pairs' in token_data:
            print(Fore.YELLOW + f"\n  Token Address: {token_address}")  # Print token address
            
            for pair in token_data['pairs']:
                solana_token_name = pair['baseToken']['name']  # Changed to solana_token_name
                solana_token_symbol = pair['baseToken']['symbol']  # Changed to solana_token_symbol
                solana_token_liquidity = pair['liquidity']['base']  # Changed to solana_token_liquidity
                quote_token_name = pair['quoteToken']['name']
                quote_token_symbol = pair['quoteToken']['symbol']
                quote_token_liquidity = pair['liquidity']['quote']
                usd_liquidity = pair['liquidity']['usd']
                price_usd = pair.get('priceUsd', 'Price not available')  # Get token price in USD

                # Print liquidity and price details
                print(Fore.WHITE + '-' * 50)
                print(Fore.CYAN + f"  {solana_token_name} ({solana_token_symbol}) / {quote_token_name} ({quote_token_symbol})")
                print(Fore.GREEN + f"  Price (USD): {price_usd}")
                print(Fore.GREEN + f"  Timestamp: {timestamp}")
                # print(Fore.GREEN + f"  Liquidity (Solana Token): {solana_token_liquidity}")
                # print(Fore.GREEN + f"  Liquidity (Quote Token): {quote_token_liquidity}")
                print(Fore.GREEN + f"  Liquidity (USD): {usd_liquidity}")
        else:
            print(Fore.RED + f"No liquidity pairs found for Solana token address: {token_address}")
    
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching liquidity data for Solana token address: {token_address}: {e}")

# Example: Input a Solana token contract address to fetch its liquidity and price data
solana_token_address = "4qkLHhLqrzeJCkC61XF82F4FieUzrqX6nzzEWG7rjPNC"
get_solana_token_data(solana_token_address)
