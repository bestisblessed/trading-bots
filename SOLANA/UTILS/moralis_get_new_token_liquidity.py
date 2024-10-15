import os
import json
import csv
from dotenv import load_dotenv
from moralis import sol_api
from colorama import init, Fore

# Initialize colorama for colored output
init(autoreset=True)

# Load environment variables from the .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("MORALIS_API_KEY")

# Check if API key is loaded correctly
if not api_key:
    print(Fore.RED + "Error: MORALIS_API_KEY is not set in the .env file")
    exit(1)

# Ensure the token-liquidities/ directory exists
output_dir = 'token-liquidities'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to fetch token price data from Moralis and save it to a CSV file
def get_token_price(token_address):
    try:
        # Make API call to Moralis to get token price
        response = sol_api.token.get_token_price(
            api_key=api_key,
            params={
                "network": "mainnet",  # Solana mainnet
                "address": token_address
            }
        )
        
        # Extracting data from the response
        exchange_name = response.get('exchangeName', 'N/A')
        exchange_address = response.get('exchangeAddress', 'N/A')
        native_price_value = response.get('nativePrice', {}).get('value', 'N/A')
        native_price_symbol = response.get('nativePrice', {}).get('symbol', 'N/A')
        native_price_name = response.get('nativePrice', {}).get('name', 'N/A')
        native_price_decimals = response.get('nativePrice', {}).get('decimals', 'N/A')
        usd_price = response.get('usdPrice', 'N/A')

        # Create a CSV file for the token
        csv_file_path = os.path.join(output_dir, f"{token_address}_liquidity.csv")

        # Define the header and rows for the CSV
        header = ['Token Address', 'Exchange Name', 'Exchange Address', 'Native Price Value', 'Native Price Symbol', 'Native Price Name', 'Native Price Decimals', 'USD Price']
        row = [token_address, exchange_name, exchange_address, native_price_value, native_price_symbol, native_price_name, native_price_decimals, usd_price]

        # Write to the CSV file
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(row)

        print(Fore.GREEN + f"Data for token {token_address} saved to {csv_file_path}")
    
    except Exception as e:
        print(Fore.RED + f"Error fetching or saving data for token {token_address}: {e}")

# Example usage with a given Solana token address
# token_address = 'HjbVJCYXKukvMf3PHjvK9FoJjzmgZPkXgtNiMkxapump'  # Example token address
token_address = 'Csr24afRg9jZnLA4m2VcgdWsEiSewsjXmaZ8zbcLpump'  # Example token address
get_token_price(token_address)
