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
    'outputMint': '4qkLHhLqrzeJCkC61XF82F4FieUzrqX6nzzEWG7rjPNC',
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

# print(f"\nTransaction sent: https://explorer.solana.com/tx/{transaction_id}")

# swapTransaction = base64.b64decode(swapTransaction)
# print('2进制:',swapTransaction)
# txn=transaction_id
# print('反序列化：',txn)
# txn.recent_blockhash=client.get_latest_blockhash().value.blockhash
# print('添加blockhash:',txn)
# txn.sign(sender)
# print('签名',txn)
# txn=txn.serialize()
# print('序列化',txn)
# hash=client.send_raw_transaction(txn)
# print(hash.value)
# print(transaction_id)
# print(signed_txn)


# import os
# import requests
# import base64
# from solders.keypair import Keypair
# from solders.pubkey import Pubkey
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

# # quote
# url = 'https://quote-api.jup.ag/v6/quote'
# params = {
#     'inputMint': 'Z6akXpS92DH5FWFHVU6YYGLJd2XaPo1vZdyF6JDpump',  # TRX mint address
#     'outputMint': 'So11111111111111111111111111111111111111112',  # SOL mint address
#     'amount': str(int(64000)),  # Number of input tokens to sell
#     'slippageBps': '100'  # 1% slippage
# }
# response = requests.get(url, params=params)
# quoteResponse = response.json()

# # Print the response for debugging
# print("Quote Response:", json.dumps(quoteResponse, indent=4))

# # swap
# url = 'https://quote-api.jup.ag/v6/swap'
# payload = {
#     'userPublicKey': str(sender.pubkey()),
#     'quoteResponse': quoteResponse,
# }
# response = requests.post(url, json=payload)
# data = response.json()

# # Print the response for debugging
# print("Swap Response:", json.dumps(data, indent=4))

# # Handle the response
# if 'swapTransaction' in data:
#     swapTransaction = data['swapTransaction']
#     raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))
#     signature = sender.sign_message(message.to_bytes_versioned(raw_transaction.message))
#     signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])
#     opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
#     result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)
#     transaction_id = json.loads(result.to_json())['result']
#     print('Transaction ID: ', transaction_id)
# else:
#     print("Error: Swap transaction not found in response")
#     # Optionally, you can also print more details to understand what went wrong
#     print("Detailed Error Response:", json.dumps(data, indent=4))