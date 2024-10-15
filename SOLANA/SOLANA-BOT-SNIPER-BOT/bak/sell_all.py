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

# # Load environment variables
# load_dotenv()
# private_key = os.getenv('MY_BOT_WALLET_PRIVATE_KEY')

# if not private_key:
#     raise ValueError("WALLET_PRIVATE_KEY not found in the .env file")

# # Solana client
# client = Client("https://api.mainnet-beta.solana.com")
# sender = Keypair.from_base58_string(private_key)

# # Wallet and file paths
# wallet_address = '7Qq8RTV2ZP3niS1xmrvDf5PemARSJamWk3gVbECP3yaE'
# file_path = f'./data/{wallet_address}_token_balances.json'

# # List of mint addresses to process
# mint_addresses = [
#     "7nWspu6U3xW3y4uc9ffVi8PtKt4jvfHpCo8tRqsDpump",  # Sirius The Dog Star
#     "DjdnBtLiktxpcnfMatnjbuCvZbuTb2A2qZoLLNu5KvQm",  # SOLA AOI👙
#     # "4VrYoRjkGXvHxbdKNBKYFyNNhKxrmukZh2Jsubfmpump",  # Aitrolls
#     # "5YzQjNqUfQ87m38xejJsUy35b8DsihYvN2ajinMjfmfh",  # Puffy
#     "GR4SFnwXT4BxXRVvV7ySuWUnonuyKEokrQGHLTZFJe5F"   # 🤩Soly The Mascot
# ]

# # Load token balances
# with open(file_path, 'r') as f:
#     token_balances = json.load(f)

# # Iterate through each mint address and process the sale
# for mint_address in mint_addresses:
#     balance = None
#     decimals = None
#     portfolio_token = None

#     # Find the token in the portfolio
#     for token in token_balances:
#         if token['mint'] == mint_address:
#             balance = float(token['amount'])
#             decimals = int(token['decimals'])
#             portfolio_token = token
#             break

#     if balance is None or decimals is None:
#         print(f"Mint address {mint_address} not found in the portfolio. Skipping...")
#         continue

#     # Print token balance and details
#     print(f"\nProcessing token with mint address: {mint_address}")
#     print(f"Balance: {balance}")
#     print(f"Decimals: {decimals}")

#     # Sell 100% of the balance
#     sell_amount = balance*.9
#     print(f"Selling 95% of balance: {sell_amount}")

#     # Calculate the raw sell amount
#     sell_amount_raw = int(sell_amount * 10**decimals)
#     print(f"Sell amount raw: {sell_amount_raw}")

#     # Get quote for swapping the token to SOL
#     url = 'https://quote-api.jup.ag/v6/quote'
#     params = {
#         'inputMint': mint_address,
#         'outputMint': 'So11111111111111111111111111111111111111112',  # Converting to SOL
#         'amount': sell_amount_raw,  # Sell all tokens
#         'slippageBps': '200'  # 2% slippage
#     }
#     response = requests.get(url, params=params)
#     quoteResponse = response.json()

#     # Small delay after fetching quote data
#     time.sleep(2)

#     # Execute the swap
#     url = 'https://quote-api.jup.ag/v6/swap'
#     payload = {
#         'userPublicKey': str(sender.pubkey()),
#         'quoteResponse': quoteResponse,
#     }
#     response = requests.post(url, json=payload)
#     data = response.json()
#     swapTransaction = data['swapTransaction']

#     # Sign and send the transaction
#     raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))
#     signature = sender.sign_message(message.to_bytes_versioned(raw_transaction.message))
#     signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])
#     opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
#     result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)

#     # Get and print transaction ID
#     transaction_id = json.loads(result.to_json())['result']
#     print('Transaction ID: ', transaction_id)
#     time.sleep(5)
import json
import os
import requests, base64
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solana.rpc.commitment import Processed
from solders.transaction import VersionedTransaction
from solders import message
from solana.rpc.types import TxOpts
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
private_key = os.getenv('MY_BOT_WALLET_PRIVATE_KEY')

if not private_key:
    raise ValueError("WALLET_PRIVATE_KEY not found in the .env file")

# Solana client
client = Client("https://api.mainnet-beta.solana.com")
sender = Keypair.from_base58_string(private_key)

# Wallet and file paths
wallet_address = '7Qq8RTV2ZP3niS1xmrvDf5PemARSJamWk3gVbECP3yaE'
file_path = f'./data/{wallet_address}_token_balances.json'

# List of mint addresses to process
mint_addresses = [
    "5YzQjNqUfQ87m38xejJsUy35b8DsihYvN2ajinMjfmfh",  # Sirius The Dog Star
    # "DjdnBtLiktxpcnfMatnjbuCvZbuTb2A2qZoLLNu5KvQm",  # SOLA AOI👙
    # "GR4SFnwXT4BxXRVvV7ySuWUnonuyKEokrQGHLTZFJe5F"   # 🤩Soly The Mascot
]

# Load token balances
with open(file_path, 'r') as f:
    token_balances = json.load(f)

# Iterate through each mint address and process the sale
for mint_address in mint_addresses:
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

    if balance is None or decimals is None:
        print(f"Mint address {mint_address} not found in the portfolio. Skipping...")
        continue

    # Print token balance and details
    print(f"\nProcessing token with mint address: {mint_address}")
    print(f"Balance: {balance}")
    print(f"Decimals: {decimals}")

    # Sell 100% of the balance (change to 0.95 if you want to sell 95%)
    sell_amount = balance
    print(f"Selling 100% of balance: {sell_amount}")

    # Calculate the raw sell amount
    sell_amount_raw = int(sell_amount * 10**decimals)
    print(f"Sell amount raw: {sell_amount_raw}")

    try:
        # Get quote for swapping the token to SOL
        url = 'https://quote-api.jup.ag/v6/quote'
        params = {
            'inputMint': mint_address,
            'outputMint': 'So11111111111111111111111111111111111111112',  # Converting to SOL
            'amount': sell_amount_raw,  # Sell all tokens
            'slippageBps': '500'  # 5% slippage (adjustable)
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # Ensure request is successful

        quoteResponse = response.json()

        if not quoteResponse.get("data"):
            print(f"No quote data returned for {mint_address}. Skipping...")
            continue

        # Small delay after fetching quote data
        time.sleep(2)

        # Execute the swap
        url = 'https://quote-api.jup.ag/v6/swap'
        payload = {
            'userPublicKey': str(sender.pubkey()),
            'quoteResponse': quoteResponse,
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Ensure the swap request is successful

        data = response.json()
        swapTransaction = data.get('swapTransaction')

        if not swapTransaction:
            print(f"No swap transaction data returned for {mint_address}. Skipping...")
            continue

        # Sign and send the transaction
        raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))
        signature = sender.sign_message(message.to_bytes_versioned(raw_transaction.message))
        signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])
        opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)

        # Send the transaction
        result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)

        # Get and print transaction ID
        transaction_id = json.loads(result.to_json())['result']
        print('Transaction ID: ', transaction_id)
        time.sleep(5)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching swap quote for {mint_address}: {e}")
    except Exception as e:
        print(f"Error during the swap for {mint_address}: {e}")

    # Delay to prevent rate limiting or too many requests
    time.sleep(5)
