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

# 'So11111111111111111111111111111111111111112', # SOL
# 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v', # USDC
# 'Z6akXpS92DH5FWFHVU6YYGLJd2XaPo1vZdyF6JDpump', # TRX
# '4qkLHhLqrzeJCkC61XF82F4FieUzrqX6nzzEWG7rjPNC', # WAGA
# '4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R' # RAY

# Load environment variables from .env file
load_dotenv()

# Get the private key from the .env file
private_key = os.getenv('WALLET_PRIVATE_KEY')

if not private_key:
    raise ValueError("WALLET_PRIVATE_KEY not found in the .env file")

client = Client("https://api.mainnet-beta.solana.com")
sender = Keypair.from_base58_string(private_key)

#quote
url = 'https://quote-api.jup.ag/v6/quote'
params = {
    'inputMint': 'So11111111111111111111111111111111111111112',
    'outputMint': '5YzQjNqUfQ87m38xejJsUy35b8DsihYvN2ajinMjfmfh',
    # 'amount': str(int(54000 * 10**6)), # Number of input tokens to sell
    'amount': str(int(0.01 * 10**9)), # Number of eth to swap
    'slippageBps': '100'  # 1% slippage
}
response = requests.get(url, params=params)
quoteResponse = response.json()
# print(quoteResponse)

#swap
url = 'https://quote-api.jup.ag/v6/swap'
payload = {
    'userPublicKey': str(sender.pubkey()),
    'quoteResponse': quoteResponse,
}
response = requests.post(url, json=payload)
data = response.json()
swapTransaction = data['swapTransaction']
# print(swapTransaction)
raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))
signature = sender.sign_message(message.to_bytes_versioned(raw_transaction.message))
signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])
opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)
transaction_id = json.loads(result.to_json())['result']
print('Transaction ID: ', transaction_id)



# import os
# import requests, base64
# from solders.keypair import Keypair
# from solana.rpc.api import Client
# import json
# from solders.transaction import VersionedTransaction
# from solders import message
# from solana.rpc.types import TxOpts
# from solana.rpc.commitment import Processed
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Get the private key from the .env file
# private_key = os.getenv('WALLET_PRIVATE_KEY')

# if not private_key:
#     raise ValueError("WALLET_PRIVATE_KEY not found in the .env file")

# client = Client("https://api.mainnet-beta.solana.com")
# sender = Keypair.from_base58_string(private_key)

# # Fetching swap quote from Raydium
# quote_url = 'https://api.raydium.io/v2/swap/quote'
# params = {
#     'inputMint': 'So11111111111111111111111111111111111111112',  # SOL
#     # 'outputMint': '4qkLHhLqrzeJCkC61XF82F4FieUzrqX6nzzEWG7rjPNC',  # WAGA
#     'outputMint': '5YzQjNqUfQ87m38xejJsUy35b8DsihYvN2ajinMjfmfh',
#     'amount': str(int(0.005 * 10**9)),  # Swapping 0.005 SOL
#     'slippage': 1  # 1% slippage
# }
# response = requests.get(quote_url, params=params)
# quoteResponse = response.json()

# # Debug: Print the full response to inspect its structure
# print("Full quote response:", json.dumps(quoteResponse, indent=2))

# # Check if 'outAmount' is in the response
# if 'outAmount' not in quoteResponse:
#     raise ValueError("The key 'outAmount' is missing in the quote response. Response received: {}".format(quoteResponse))

# # Preparing swap transaction
# swap_url = 'https://api.raydium.io/v2/swap/transaction'
# payload = {
#     'owner': str(sender.pubkey()),
#     'inputMint': 'So11111111111111111111111111111111111111112',
#     'outputMint': '5YzQjNqUfQ87m38xejJsUy35b8DsihYvN2ajinMjfmfh',
#     'amountIn': str(int(0.005 * 10**9)),  # Amount of SOL to swap
#     'minAmountOut': str(int(quoteResponse['outAmount'] * 0.99)),  # 1% slippage
#     'swapMode': 'ExactIn',
# }
# response = requests.post(swap_url, json=payload)
# data = response.json()

# # Debug: Print the full response to inspect its structure
# print("Full swap response:", json.dumps(data, indent=2))

# if 'error' in data:
#     raise ValueError(f"Error in swap transaction: {data['error']}")

# swapTransaction = data['swapTransaction']
# raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))
# signature = sender.sign_message(message.to_bytes_versioned(raw_transaction.message))
# signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])
# opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)

# result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)
# transaction_id = json.loads(result.to_json())['result']

# print(f"Transaction sent: https://explorer.solana.com/tx/{transaction_id}")





# # Both combined in a function

# # def swap_waga_to_sol():
# #     import os
# #     import requests, base64
# #     from solders.keypair import Keypair
# #     from solana.rpc.api import Client
# #     import json
# #     from solders.transaction import VersionedTransaction
# #     from solders import message
# #     from solana.rpc.types import TxOpts
# #     from solana.rpc.commitment import Processed
# #     from dotenv import load_dotenv

# #     # Load environment variables from .env file
# #     load_dotenv()

# #     # Get the private key from the .env file
# #     private_key = os.getenv('WALLET_PRIVATE_KEY')

# #     if not private_key:
# #         raise ValueError("WALLET_PRIVATE_KEY not found in the .env file")

# #     client = Client("https://api.mainnet-beta.solana.com")
# #     sender = Keypair.from_base58_string(private_key)

# #     # Fetching swap quote from Raydium for WAGA to SOL
# #     quote_url = 'https://api.raydium.io/v2/swap/quote'
# #     params = {
# #         'inputMint': '4qkLHhLqrzeJCkC61XF82F4FieUzrqX6nzzEWG7rjPNC',  # WAGA
# #         'outputMint': 'So11111111111111111111111111111111111111112',  # SOL
# #         'amount': str(int(0.005 * 10**9)),  # Swapping 0.005 WAGA to SOL
# #         'slippage': 1  # 1% slippage
# #     }
# #     response = requests.get(quote_url, params=params)
# #     quoteResponse = response.json()
# #     print(quoteResponse)

# #     if 'error' in quoteResponse:
# #         raise ValueError(f"Error fetching quote: {quoteResponse['error']}")

# #     # Preparing swap transaction
# #     swap_url = 'https://api.raydium.io/v2/swap/transaction'
# #     payload = {
# #         'owner': str(sender.pubkey()),
# #         'inputMint': '4qkLHhLqrzeJCkC61XF82F4FieUzrqX6nzzEWG7rjPNC',
# #         'outputMint': 'So11111111111111111111111111111111111111112',
# #         'amountIn': str(int(0.005 * 10**9)),  # Amount of WAGA to swap
# #         'minAmountOut': str(int(quoteResponse['outAmount'] * 0.99)),  # 1% slippage
# #         'swapMode': 'ExactIn',
# #     }
# #     response = requests.post(swap_url, json=payload)
# #     data = response.json()
# #     print(data)

# #     if 'error' in data:
# #         raise ValueError(f"Error in swap transaction: {data['error']}")

# #     swapTransaction = data['swapTransaction']
# #     raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))
# #     signature = sender.sign_message(message.to_bytes_versioned(raw_transaction.message))
# #     signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])
# #     opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)

# #     result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)
# #     transaction_id = json.loads(result.to_json())['result']

# #     print(f"Transaction sent: https://explorer.solana.com/tx/{transaction_id}")

# # # Call the function
# # swap_waga_to_sol()
