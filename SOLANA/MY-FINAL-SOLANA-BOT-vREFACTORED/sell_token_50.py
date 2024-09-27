import os
import requests, base64
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
import time, json
from solders.transaction import VersionedTransaction
from solders import message
from solana.rpc.types import TxOpts
from solana.rpc.commitment import Processed
from dotenv import load_dotenv
import sys
from moralis import sol_api
from colorama import init, Fore, Style
import datetime
from moralis import sol_api
from solana.rpc.core import RPCException

# Initialize colorama
init(autoreset=True)

# Load environment variables from the .env file
# load_dotenv()

# Get the absolute path to the .env file
env_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.env'))

# Load environment variables from the .env file
load_dotenv(env_file_path)

# Check if the mint address argument is provided
if len(sys.argv) < 2:
    print(Fore.RED + "Error: No mint address provided. Usage: python sell_token.py <mint_address>")
    sys.exit(1)

# Get the mint address from the command line argument
mint_address = sys.argv[1]

# Get the API key and wallet address from the environment variables
api_key = os.getenv("MORALIS_API_KEY")
wallet_address = os.getenv("MY_BOT_WALLET_ADDRESS")
private_key = os.getenv('MY_BOT_KEY')

if not private_key:
    raise ValueError("MY_BOT_KEY not found in the .env file")
if not wallet_address:
    raise ValueError("MY_BOT_WALLET_ADDRESS not found in the .env file")

# # Ensure the data directory exists
# data_dir = 'wallets'
# if not os.path.exists(data_dir):
#     os.makedirs(data_dir)

# # Define file paths
# output_path = os.path.join(data_dir, f'{wallet_address}_token_balances.json')
# # buy_prices_path = os.path.join(data_dir, 'buy_prices.json')

data_dir = os.path.abspath('wallets')
output_path = os.path.join(data_dir, f'{wallet_address}_token_balances.json')

# Fetch the portfolio balance using Moralis
params = {
    "address": wallet_address,
    "network": "mainnet",
}
result = sol_api.account.get_portfolio(api_key=api_key, params=params)

# Extract token balances from the portfolio
tokens = result.get('tokens', [])

# Save the current token balances to a JSON file
with open(output_path, 'w') as f:
    json.dump(tokens, f, indent=2)
print(f'Current token balances saved to {output_path}')

# Find the specific token in the portfolio
token = next((token for token in tokens if token.get('mint') == mint_address), None)

if not token:
    print(Fore.RED + f"Token with mint address {mint_address} not found in portfolio.")
    sys.exit(1)

# Dexscreener API endpoint for Solana tokens
dexscreener_api_endpoint = 'https://api.dexscreener.com/latest/dex/tokens'

# Skip native SOL tokens (starting with "So1")
if mint_address.startswith("So1"):
    print(Fore.RED + f"Skipping token with address starting with 'So1': {mint_address}")
    sys.exit(1)

# Check if buy prices exist, otherwise initialize an empty dictionary
# if os.path.exists(buy_prices_path):
#     with open(buy_prices_path, 'r') as f:
#         buy_prices = json.load(f)
# else:
#     buy_prices = {}

try:
    # Make API request to Dexscreener for the Solana token address
    response = requests.get(f'{dexscreener_api_endpoint}/{mint_address}')
    response.raise_for_status()  # Raise an exception for HTTP errors
    token_data = response.json()

    # Generate a timestamp for when the data is fetched
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # Check if token data and pairs exist and are not None
    if token_data and 'pairs' in token_data and token_data['pairs']:
        print(Fore.WHITE + '-' * 50)
        print(Fore.CYAN + f"  TOKEN ADDRESS: {mint_address}")  # Print token address
        
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
        # if mint_address not in buy_prices:
        #     # Save token details to the buy_prices.json file
        #     buy_prices[mint_address] = {
        #         "name": solana_token_name,
        #         "symbol": solana_token_symbol,
        #         "price_usd": price_usd,
        #         "liquidity_usd": usd_liquidity,
        #         "timestamp": timestamp
        #     }
        #     print(Fore.BLACK + f"  Added token details for {solana_token_name} ({solana_token_symbol}) to buy_prices.json")

        #     # Save the buy prices back to the buy_prices.json file
        #     with open(buy_prices_path, 'w') as f:
        #         json.dump(buy_prices, f, indent=2)

        # Print liquidity and price details
        print(Fore.YELLOW + f"  {solana_token_name} ({solana_token_symbol}) / {quote_token_name} ({quote_token_symbol})")
        print(Fore.GREEN + f"  Price (USD): {price_usd}")
        print(Fore.GREEN + f"  Timestamp: {timestamp}")
        print(Fore.GREEN + f"  Liquidity (Solana Token): {solana_token_liquidity}")
        print(Fore.GREEN + f"  Liquidity (Quote Token): {quote_token_liquidity}")
        print(Fore.GREEN + f"  Liquidity (USD): {usd_liquidity}")
    else:
        print(Fore.WHITE + '-' * 50)
        print(Fore.RED + f"No liquidity pairs found for: {mint_address}")

except requests.exceptions.RequestException as e:
    print(Fore.RED + f"Error fetching liquidity data for Solana token address: {mint_address}: {e}")

# Done processing the token
print(f"Finished processing liquidity for {mint_address}.")

### SELL NOW ###
# Initialize the Solana client
client = Client("https://api.mainnet-beta.solana.com")

# Create the Keypair object from the private key
sender = Keypair.from_base58_string(private_key)

# File path to token balances
# file_path = f'./wallets/{wallet_address}_token_balances.json'
file_path = os.path.join(data_dir, f'{wallet_address}_token_balances.json')

# Load token balances from the file
with open(file_path, 'r') as f:
    token_balances = json.load(f)

# Get the mint address from the command line argument
mint_address = sys.argv[1]

# Initialize variables
balance = None
decimals = None
portfolio_token = None

# Find the token in the portfolio
for token in token_balances:
    if token['mint'] == mint_address:
        balance = float(token['amount'])
        decimals = int(token['decimals'])
        symbol = token.get('symbol', 'Unknown')  # Get the token symbol, default to 'Unknown'
        portfolio_token = token
        break

# Raise an error if the token is not found
if balance is None or decimals is None:
    raise ValueError(f"Mint address {mint_address} not found in the portfolio.")

# print(f"Balance: {balance}")
# print(f"Decimals: {decimals}")
print(f"Token Symbol: {symbol}")

# Calculate the sell amount
sell_amount = float(balance) * 0.5
print(f"Selling 50% of {symbol}: {sell_amount}")

# Convert to raw token amount
sell_amount_raw = int(sell_amount * 10**decimals)
# print(f"Sell amount raw: {sell_amount_raw}")

# Prepare the quote API request
url = 'https://quote-api.jup.ag/v6/quote'
params = {
    'inputMint': mint_address,
    'outputMint': 'So11111111111111111111111111111111111111112',  # Converting to SOL
    'amount': sell_amount_raw,  # Sell 50% of tokens
    'slippageBps': '500'  # 1% slippage
}

time.sleep(2)

try:
    # Fetch the quote for the swap
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise error for failed requests
    quoteResponse = response.json()

    # Small delay after fetching quote data
    time.sleep(2)

    # Prepare the swap API request
    url = 'https://quote-api.jup.ag/v6/swap'
    payload = {
        'userPublicKey': str(sender.pubkey()),
        'quoteResponse': quoteResponse,
    }

    # Execute the swap
    response = requests.post(url, json=payload)
    response.raise_for_status()  # Raise error for failed requests
    data = response.json()

    # Deserialize the swap transaction
    swapTransaction = data['swapTransaction']
    raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))
    
    # Sign the transaction
    signature = sender.sign_message(message.to_bytes_versioned(raw_transaction.message))
    signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])

    # Send the signed transaction
    opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
    result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)

    # Get the transaction ID
    result_raw_output = json.loads(result.to_json())
    print(result_raw_output)
    transaction_id = json.loads(result.to_json())['result']
    # print(f"Ran sell_token_100.py on {mint_address}")
    print('Transaction ID: ', transaction_id)

except RPCException as rpc_error:
    # Handle Solana RPC-specific errors, e.g., frozen accounts or failed transactions
    # print(f"Transaction failed with RPC error: {rpc_error}")
    print(f"Transaction failed with RPC error")
except requests.exceptions.RequestException as req_error:
    # Handle errors during HTTP requests (quote or swap API)
    # print(f"Request failed: {req_error}")
    print(f"Request failed")
except Exception as e:
    # Handle any other unexpected errors
    # print(f"An error occurred: {e}")
    print(f"An error occurred")



