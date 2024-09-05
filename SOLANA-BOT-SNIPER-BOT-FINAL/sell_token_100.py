# import json
# import os
# import requests, base64
# from solders.keypair import Keypair
# from solders.pubkey import Pubkey
# from solana.rpc.api import Client
# from solana.rpc.commitment import Processed
# from solders.transaction import VersionedTransaction
# from solders import message
# from solana.rpc.types import TxOpts
# from dotenv import load_dotenv
# import time
# import sys
# from moralis import sol_api

# # Load environment variables from the .env file
# load_dotenv()

# # Get the private key and wallet address from the .env file
# private_key = os.getenv('MY_BOT_WALLET_PRIVATE_KEY')
# wallet_address = os.getenv('MY_BOT_WALLET_ADDRESS')

# # Check if both private key and wallet address were loaded correctly
# if not private_key:
#     raise ValueError("MY_BOT_WALLET_PRIVATE_KEY not found in the .env file")
# if not wallet_address:
#     raise ValueError("MY_BOT_WALLET_ADDRESS not found in the .env file")

# # Initialize the Solana client
# client = Client("https://api.mainnet-beta.solana.com")

# # Create the Keypair object from the private key
# sender = Keypair.from_base58_string(private_key)

# # load_dotenv()
# # private_key = os.getenv('MY_BOT_WALLET_PRIVATE_KEY')

# # if not private_key:
# #     raise ValueError("WALLET_PRIVATE_KEY not found in the .env file")

# # client = Client("https://api.mainnet-beta.solana.com")
# # sender = Keypair.from_base58_string(private_key)

# # wallet_address = '7Qq8RTV2ZP3niS1xmrvDf5PemARSJamWk3gVbECP3yaE'
# file_path = f'./data/{wallet_address}_token_balances.json'

# with open(file_path, 'r') as f:
#     token_balances = json.load(f)

# mint_address = sys.argv[1]

# balance = None
# decimals = None
# portfolio_token = None

# for token in token_balances:
#     if token['mint'] == mint_address:
#         balance = float(token['amount'])
#         decimals = int(token['decimals'])
#         portfolio_token = token
#         break

# if balance is None or decimals is None:
#     raise ValueError(f"Mint address {mint_address} not found in the portfolio.")

# print(f"Balance: {balance}")
# print(f"Decimals: {decimals}")

# sell_amount = float(balance) * 0.5
# print(f"Selling 50% of balance: {sell_amount}")

# sell_amount_raw = int(sell_amount * 10**decimals)
# print(f"Sell amount raw: {sell_amount_raw}")

# url = 'https://quote-api.jup.ag/v6/quote'
# params = {
#     'inputMint': mint_address,
#     'outputMint': 'So11111111111111111111111111111111111111112',  # Converting to SOL
#     'amount': sell_amount_raw,  # Sell all tokens
#     'slippageBps': '250'  # 1% slippage
# }
# response = requests.get(url, params=params)
# quoteResponse = response.json()
# time.sleep(2)  # Small delay after fetching quote data
# url = 'https://quote-api.jup.ag/v6/swap'
# payload = {
#     'userPublicKey': str(sender.pubkey()),
#     'quoteResponse': quoteResponse,
# }
# response = requests.post(url, json=payload)
# data = response.json()
# swapTransaction = data['swapTransaction']
# raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))
# signature = sender.sign_message(message.to_bytes_versioned(raw_transaction.message))
# signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])
# opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
# result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)
# transaction_id = json.loads(result.to_json())['result']
# print('Transaction ID: ', transaction_id)
import json
import os
import requests
import base64
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solana.rpc.commitment import Processed
from solders.transaction import VersionedTransaction
from solders import message
from solana.rpc.types import TxOpts
from dotenv import load_dotenv
import time
import sys
from moralis import sol_api
from solana.rpc.core import RPCException

# Load environment variables from the .env file
load_dotenv()

# Get the private key and wallet address from the .env file
private_key = os.getenv('MY_BOT_WALLET_PRIVATE_KEY')
wallet_address = os.getenv('MY_BOT_WALLET_ADDRESS')

# Check if both private key and wallet address were loaded correctly
if not private_key:
    raise ValueError("MY_BOT_WALLET_PRIVATE_KEY not found in the .env file")
if not wallet_address:
    raise ValueError("MY_BOT_WALLET_ADDRESS not found in the .env file")

# Initialize the Solana client
client = Client("https://api.mainnet-beta.solana.com")

# Create the Keypair object from the private key
sender = Keypair.from_base58_string(private_key)

# File path to token balances
file_path = f'./data/{wallet_address}_token_balances.json'

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
        portfolio_token = token
        break

# Raise an error if the token is not found
if balance is None or decimals is None:
    raise ValueError(f"Mint address {mint_address} not found in the portfolio.")

print(f"Balance: {balance}")
print(f"Decimals: {decimals}")

# Calculate the sell amount
sell_amount = float(balance) * 0.5
print(f"Selling 50% of balance: {sell_amount}")

# Convert to raw token amount
sell_amount_raw = int(sell_amount * 10**decimals)
print(f"Sell amount raw: {sell_amount_raw}")

# Prepare the quote API request
url = 'https://quote-api.jup.ag/v6/quote'
params = {
    'inputMint': mint_address,
    'outputMint': 'So11111111111111111111111111111111111111112',  # Converting to SOL
    'amount': sell_amount_raw,  # Sell 50% of tokens
    'slippageBps': '250'  # 1% slippage
}

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
    transaction_id = json.loads(result.to_json())['result']
    print(f"Ran sell_token_100.py on {mint_address}")
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
