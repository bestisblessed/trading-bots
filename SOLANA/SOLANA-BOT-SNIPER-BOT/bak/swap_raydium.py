# # # import os
# # # import requests, base64
# # # from solders.keypair import Keypair
# # # from solders.pubkey import Pubkey
# # # from solana.rpc.api import Client
# # # import time, json
# # # from solders.transaction import VersionedTransaction
# # # from solders import message
# # # from solana.rpc.types import TxOpts
# # # from solana.rpc.commitment import Processed
# # # from dotenv import load_dotenv

# # # # 'So11111111111111111111111111111111111111112', # SOL
# # # # 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v', # USDC
# # # # 'Z6akXpS92DH5FWFHVU6YYGLJd2XaPo1vZdyF6JDpump', # TRX
# # # # '4qkLHhLqrzeJCkC61XF82F4FieUzrqX6nzzEWG7rjPNC', # WAGA
# # # # '4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R' # RAY

# # # # Load environment variables from .env file
# # # load_dotenv()

# # # # Get the private key from the .env file
# # # private_key = os.getenv('MY_BOT_WALLET_PRIVATE_KEY')

# # # if not private_key:
# # #     raise ValueError("MY_BOT_WALLET_PRIVATE_KEY not found in the .env file")

# # # client = Client("https://api.mainnet-beta.solana.com")
# # # sender = Keypair.from_base58_string(private_key)

# # # #quote
# # # url = 'https://quote-api.jup.ag/v6/quote'
# # # params = {
# # #     'inputMint': 'So11111111111111111111111111111111111111112',
# # #     'outputMint': 'DHzMKeQzZQKZfetKydER4EkyzDtgzvzxkuVr9eRzqWQS',
# # #     # 'amount': str(int(54000 * 10**6)), # Number of input tokens to sell
# # #     'amount': str(int(0.005 * 10**9)), # Number of SOL to swap
# # #     'slippageBps': '200'  # 1% slippage
# # # }
# # # response = requests.get(url, params=params)
# # # quoteResponse = response.json()
# # # # print(quoteResponse)

# # # #swap
# # # url = 'https://quote-api.jup.ag/v6/swap'
# # # payload = {
# # #     'userPublicKey': str(sender.pubkey()),
# # #     'quoteResponse': quoteResponse,
# # # }
# # # response = requests.post(url, json=payload)
# # # data = response.json()
# # # swapTransaction = data['swapTransaction']
# # # # print(swapTransaction)
# # # raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))
# # # signature = sender.sign_message(message.to_bytes_versioned(raw_transaction.message))
# # # signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])
# # # opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
# # # result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)
# # # transaction_id = json.loads(result.to_json())['result']
# # # print('Transaction ID: ', transaction_id)
# # import os
# # import requests, base64
# # import json
# # import time
# # from solders.keypair import Keypair
# # from solana.rpc.api import Client
# # from solders.transaction import VersionedTransaction
# # from solders.signature import Signature
# # from solders import message
# # from solana.rpc.types import TxOpts
# # from solana.rpc.commitment import Processed
# # from dotenv import load_dotenv

# # # Load environment variables from .env file
# # load_dotenv()

# # # Get the private key from the .env file
# # private_key = os.getenv('MY_BOT_WALLET_PRIVATE_KEY')

# # if not private_key:
# #     raise ValueError("MY_BOT_WALLET_PRIVATE_KEY not found in the .env file")

# # client = Client("https://api.mainnet-beta.solana.com")
# # sender = Keypair.from_base58_string(private_key)

# # # Input token mint address (replace this with your desired token's mint address)
# # # mint_address = input("Enter the token mint address to buy: ")
# # mint_address = 'DHzMKeQzZQKZfetKydER4EkyzDtgzvzxkuVr9eRzqWQS'

# # # Jupiter API - Get a quote for buying the token
# # url = 'https://quote-api.jup.ag/v6/quote'
# # params = {
# #     'inputMint': 'So11111111111111111111111111111111111111112',  # SOL
# #     'outputMint': mint_address,
# #     'amount': str(int(0.005 * 10**9)),  # Amount of SOL to swap (e.g., 0.005 SOL)
# #     'slippageBps': '200'  # 2% slippage
# # }
# # response = requests.get(url, params=params)
# # quoteResponse = response.json()

# # # Print the quoteResponse for debugging
# # print("Quote Response:", json.dumps(quoteResponse, indent=2))

# # # Jupiter API - Get the swap transaction
# # url = 'https://quote-api.jup.ag/v6/swap'
# # payload = {
# #     'userPublicKey': str(sender.pubkey()),
# #     'quoteResponse': quoteResponse,
# # }
# # response = requests.post(url, json=payload)
# # data = response.json()

# # # Extract the swap transaction
# # swapTransaction = data['swapTransaction']

# # # Decode the transaction
# # raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))

# # # Sign the transaction
# # signature = Signature(sender.sign_message(message.to_bytes_versioned(raw_transaction.message)))
# # signed_txn = VersionedTransaction(raw_transaction.message, [signature])

# # # Send the signed transaction
# # opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
# # result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)

# # # Print the transaction ID
# # transaction_id = json.loads(result.to_json())['result']
# # print('Transaction ID:', transaction_id)
# import os
# import requests, base64
# import json
# from solders.keypair import Keypair
# from solana.rpc.api import Client
# from solders.transaction import VersionedTransaction
# from solders import message
# from solana.rpc.types import TxOpts
# from solana.rpc.commitment import Processed
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Get the private key from the .env file
# private_key = os.getenv('MY_BOT_WALLET_PRIVATE_KEY')

# if not private_key:
#     raise ValueError("MY_BOT_WALLET_PRIVATE_KEY not found in the .env file")

# client = Client("https://api.mainnet-beta.solana.com")
# sender = Keypair.from_base58_string(private_key)

# # Input token mint address (replace this with your desired token's mint address)
# # mint_address = input("Enter the token mint address to buy: ")
# mint_address = 'DHzMKeQzZQKZfetKydER4EkyzDtgzvzxkuVr9eRzqWQS'

# # Jupiter API - Get a quote for buying the token
# url = 'https://quote-api.jup.ag/v6/quote'
# params = {
#     'inputMint': 'So11111111111111111111111111111111111111112',  # SOL
#     'outputMint': mint_address,
#     'amount': str(int(0.005 * 10**9)),  # Amount of SOL to swap (e.g., 0.005 SOL)
#     'slippageBps': '200'  # 2% slippage
# }
# response = requests.get(url, params=params)
# quoteResponse = response.json()

# # Print the quoteResponse for debugging
# print("Quote Response:", json.dumps(quoteResponse, indent=2))

# # Jupiter API - Get the swap transaction
# url = 'https://quote-api.jup.ag/v6/swap'
# payload = {
#     'userPublicKey': str(sender.pubkey()),
#     'quoteResponse': quoteResponse,
# }
# response = requests.post(url, json=payload)
# data = response.json()

# # Extract the swap transaction
# swapTransaction = data['swapTransaction']

# # Decode the transaction
# raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))

# # Sign the transaction by signing the serialized message
# signature = sender.sign_message(raw_transaction.message.serialize())  # Create signature from the serialized message
# signed_txn = VersionedTransaction(raw_transaction.message, [signature])  # Attach the signature to the transaction

# # Send the signed transaction
# opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
# result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)

# # Print the transaction ID
# transaction_id = json.loads(result.to_json())['result']
# print('Transaction ID:', transaction_id)
import os
import requests, base64
import json
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction
from solders import message
from solana.rpc.api import Client
from solana.rpc.commitment import Processed
from solana.rpc.types import TxOpts
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()
private_key = os.getenv('MY_BOT_WALLET_PRIVATE_KEY')

if not private_key:
    raise ValueError("MY_BOT_WALLET_PRIVATE_KEY not found in the .env file")

client = Client("https://api.mainnet-beta.solana.com")
sender = Keypair.from_base58_string(private_key)

# Input token mint address (replace this with your desired token's mint address)
# mint_address = input("Enter the token mint address to buy: ")
mint_address = 'mpoxP5wyoR3eRW8L9bZjGPFtCsmX8WcqU5BHxFW1xkn'

# Jupiter API - Get a quote for buying the token
url = 'https://quote-api.jup.ag/v6/quote'
params = {
    'inputMint': 'So11111111111111111111111111111111111111112',  # SOL
    'outputMint': mint_address,
    'amount': str(int(0.001 * 10**9)),  # Swap 0.001 SOL instead of 0.005 SOL
    'slippageBps': '300'  # 2% slippage
}
response = requests.get(url, params=params)
quoteResponse = response.json()

# Print the quoteResponse for debugging
print("Quote Response:", json.dumps(quoteResponse, indent=2))

# Jupiter API - Get the swap transaction
url = 'https://quote-api.jup.ag/v6/swap'
payload = {
    'userPublicKey': str(sender.pubkey()),
    'quoteResponse': quoteResponse,
}
response = requests.post(url, json=payload)
data = response.json()

# Extract the swap transaction
swapTransaction = data['swapTransaction']

# Decode the transaction
raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))

# Sign the transaction by signing the message in versioned format
signature = sender.sign_message(message.to_bytes_versioned(raw_transaction.message))

# Populate the transaction with the signature
signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])

# Send the signed transaction
opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)

# Print the transaction ID
transaction_id = json.loads(result.to_json())['result']
print('Transaction ID:', transaction_id)
