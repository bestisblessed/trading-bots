# # # import json
# # # import os
# # # import sys
# # # import requests, base64
# # # from solders.keypair import Keypair
# # # from solana.rpc.api import Client
# # # from solana.rpc.commitment import Processed
# # # from solders.transaction import VersionedTransaction
# # # from solders import message
# # # from solana.rpc.types import TxOpts
# # # from dotenv import load_dotenv
# # # from moralis import sol_api
# # # import time

# # # # Load environment variables
# # # load_dotenv()
# # # private_key = os.getenv('MY_BOT_WALLET_PRIVATE_KEY')
# # # api_key = os.getenv("MORALIS_API_KEY")

# # # # Ensure private key is loaded
# # # if not private_key:
# # #     raise ValueError("WALLET_PRIVATE_KEY not found in the .env file")

# # # # Initialize Solana client
# # # client = Client("https://api.mainnet-beta.solana.com")
# # # sender = Keypair.from_base58_string(private_key)

# # # # Find the specific token in the portfolio
# # # # if portfolio_token['mint'] == mint_address:
# # # mint_address = '5YzQjNqUfQ87m38xejJsUy35b8DsihYvN2ajinMjfmfh'
# # # balance = 
# # # # balance = portfolio_token['amount']

# # # # Sell 90% instead
# # # decimals = int(portfolio_token['decimals'])
# # # sell_amount = float(balance) * 0.9  # Calculate 90% of the balance
# # # print(f"Selling {sell_amount} of token {portfolio_token['name']} ({portfolio_token['symbol']})")
# # # sell_amount_raw = int(sell_amount * 10**decimals)
# # # url = 'https://quote-api.jup.ag/v6/quote'
# # # params = {
# # #     'inputMint': mint_address,
# # #     'outputMint': 'So11111111111111111111111111111111111111112',  # Converting to SOL
# # #     'amount': sell_amount_raw,  # Sell all tokens
# # #     'slippageBps': '200'  # 1% slippage
# # # }
# # # response = requests.get(url, params=params)
# # # quoteResponse = response.json()
# # # time.sleep(2)  # Small delay after fetching quote data
# # # url = 'https://quote-api.jup.ag/v6/swap'
# # # payload = {
# # #     'userPublicKey': str(sender.pubkey()),
# # #     'quoteResponse': quoteResponse,
# # # }
# # # response = requests.post(url, json=payload)
# # # data = response.json()
# # # swapTransaction = data['swapTransaction']
# # # raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))
# # # signature = sender.sign_message(message.to_bytes_versioned(raw_transaction.message))
# # # signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])
# # # opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
# # # result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)
# # # transaction_id = json.loads(result.to_json())['result']
# # # print('Transaction ID: ', transaction_id)
# # # time.sleep(3)  # General de
# # import json
# # import os
# # import requests, base64
# # from solders.keypair import Keypair
# # from solana.rpc.api import Client
# # from solana.rpc.commitment import Processed
# # from solders.transaction import VersionedTransaction
# # from solders import message
# # from solana.rpc.types import TxOpts
# # from dotenv import load_dotenv
# # import time

# # # Load environment variables
# # load_dotenv()
# # private_key = os.getenv('MY_BOT_WALLET_PRIVATE_KEY')

# # if not private_key:
# #     raise ValueError("WALLET_PRIVATE_KEY not found in the .env file")

# # client = Client("https://api.mainnet-beta.solana.com")
# # sender = Keypair.from_base58_string(private_key)

# # # Path to the token balances file
# # wallet_address = '7Qq8RTV2ZP3niS1xmrvDf5PemARSJamWk3gVbECP3yaE'
# # file_path = f'./data/{wallet_address}_token_balances.json'

# # # Load token balances from the file
# # with open(file_path, 'r') as f:
# #     token_balances = json.load(f)

# # # Specify the mint address of the token you want to sell
# # mint_address = '5YzQjNqUfQ87m38xejJsUy35b8DsihYvN2ajinMjfmfh'

# # # Find the balance for the specific mint address
# # balance = None
# # decimals = None
# # portfolio_token = None

# # for token in token_balances:
# #     if token['mint'] == mint_address:
# #         balance = float(token['amount'])  # Get the balance
# #         decimals = int(token['decimals'])  # Get the decimals
# #         portfolio_token = token  # Store the token data for future reference
# #         break

# # if balance is None or decimals is None:
# #     raise ValueError(f"Mint address {mint_address} not found in the portfolio.")

# # # Sell 90% of the token balance
# # sell_amount = balance * 0.9
# # sell_amount_raw = int(sell_amount * 10**decimals)
# # print(f"Selling {sell_amount} of token {portfolio_token['name']} ({portfolio_token['symbol']})")

# # # Prepare the request to Jupiter API to get a quote
# # url = 'https://quote-api.jup.ag/v6/quote'
# # params = {
# #     'inputMint': mint_address,
# #     'outputMint': 'So11111111111111111111111111111111111111112',  # Converting to SOL
# #     'amount': sell_amount_raw,  # Sell 90% of tokens
# #     'slippageBps': '200'  # 2% slippage
# # }
# # response = requests.get(url, params=params)
# # quoteResponse = response.json()

# # # Ensure the quote response contains valid data
# # if 'data' not in quoteResponse:
# #     raise ValueError(f"Error fetching quote: {quoteResponse}")

# # # Small delay before the swap
# # time.sleep(2)

# # # Prepare the swap request to Jupiter API
# # url = 'https://quote-api.jup.ag/v6/swap'
# # payload = {
# #     'userPublicKey': str(sender.pubkey()),
# #     'quoteResponse': quoteResponse,
# # }
# # response = requests.post(url, json=payload)
# # data = response.json()

# # # Ensure valid swap response
# # if 'swapTransaction' not in data:
# #     raise ValueError(f"Error in swap: {data}")

# # # Decode and sign the swap transaction
# # swapTransaction = data['swapTransaction']
# # raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))
# # signature = sender.sign_message(message.to_bytes_versioned(raw_transaction.message))
# # signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])

# # # Send the signed transaction to the Solana network
# # opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
# # result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)

# # # Fetch transaction result
# # transaction_id = json.loads(result.to_json())['result']
# # print('Transaction ID: ', transaction_id)

# # # Delay between requests
# # time.sleep(3)
# import json
# import os
# import requests, base64
# from solders.keypair import Keypair
# from solana.rpc.api import Client
# from solana.rpc.commitment import Processed
# from solders.transaction import VersionedTransaction
# from solders import message
# from solana.rpc.types import TxOpts
# from dotenv import load_dotenv
# import time
# import sys
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
# from moralis import sol_api
# import time

# # Load environment variables
# load_dotenv()
# private_key = os.getenv('MY_BOT_WALLET_PRIVATE_KEY')

# if not private_key:
#     raise ValueError("MY_BOT_WALLET_PRIVATE_KEY not found in the .env file")

# client = Client("https://api.mainnet-beta.solana.com")
# sender = Keypair.from_base58_string(private_key)

# # Path to the token balances file
# wallet_address = '7Qq8RTV2ZP3niS1xmrvDf5PemARSJamWk3gVbECP3yaE'
# file_path = f'./data/{wallet_address}_token_balances.json'

# # Load token balances from the file
# with open(file_path, 'r') as f:
#     token_balances = json.load(f)

# # Specify the mint address of the token you want to sell
# mint_address = sys.argv[1]

# # Find the balance for the specific mint address
# balance = None
# decimals = None
# portfolio_token = None

# for token in token_balances:
#     if token['mint'] == mint_address:
#         balance = float(token['amount'])  # Get the balance
#         decimals = int(token['decimals'])  # Get the decimals
#         portfolio_token = token  # Store the token data for future reference
#         break

# if balance is None or decimals is None:
#     raise ValueError(f"Mint address {mint_address} not found in the portfolio.")

# # Sell 90% of the token balance
# sell_amount = balance * 0.8
# sell_amount_raw = int(sell_amount * 10**decimals)
# print(f"Selling {sell_amount} of token {portfolio_token['name']} ({portfolio_token['symbol']})")

# # Prepare the request to Jupiter API to get a quote
# url = 'https://quote-api.jup.ag/v6/quote'
# params = {
#     'inputMint': mint_address,
#     'outputMint': 'So11111111111111111111111111111111111111112',  # Converting to SOL
#     'amount': sell_amount_raw,  # Sell 90% of tokens
#     'slippageBps': '200'  # 2% slippage
# }
# response = requests.get(url, params=params)
# quoteResponse = response.json()

# # Check if quote was fetched correctly
# if 'routePlan' not in quoteResponse:
#     raise ValueError(f"Error fetching quote: {quoteResponse}")

# # Proceed with the swap if the quote is valid
# print(f"Received quote response: {quoteResponse}")

# # Small delay before the swap
# time.sleep(2)

# # Prepare the swap request to Jupiter API
# url = 'https://quote-api.jup.ag/v6/swap'
# payload = {
#     'userPublicKey': str(sender.pubkey()),
#     'quoteResponse': quoteResponse,
# }
# response = requests.post(url, json=payload)
# data = response.json()

# # Ensure valid swap response
# if 'swapTransaction' not in data:
#     raise ValueError(f"Error in swap: {data}")

# # Decode and sign the swap transaction
# swapTransaction = data['swapTransaction']
# raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))
# signature = sender.sign_message(message.to_bytes_versioned(raw_transaction.message))
# signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])

# # Send the signed transaction to the Solana network
# opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
# result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)

# # Fetch transaction result
# transaction_id = json.loads(result.to_json())['result']
# print('Transaction ID: ', transaction_id)

# # Delay between requests
# time.sleep(3)
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

# # Load environment variables
# load_dotenv()
# private_key = os.getenv('MY_BOT_WALLET_PRIVATE_KEY')

# if not private_key:
#     raise ValueError("WALLET_PRIVATE_KEY not found in the .env file")

# client = Client("https://api.mainnet-beta.solana.com")
# sender = Keypair.from_base58_string(private_key)

# # Path to the token balances file
# wallet_address = '7Qq8RTV2ZP3niS1xmrvDf5PemARSJamWk3gVbECP3yaE'
# file_path = f'./data/{wallet_address}_token_balances.json'

# # Load token balances from the file
# with open(file_path, 'r') as f:
#     token_balances = json.load(f)

# # Specify the mint address of the token you want to sell
# mint_address = sys.argv[1]  # Pass the mint address as an argument when running the script

# # Find the balance for the specific mint address
# balance = None
# decimals = None
# portfolio_token = None

# for token in token_balances:
#     if token['mint'] == mint_address:
#         balance = float(token['amount'])  # Get the balance
#         decimals = int(token['decimals'])  # Get the decimals
#         portfolio_token = token  # Store the token data for future reference
#         break

# if balance is None or decimals is None:
#     raise ValueError(f"Mint address {mint_address} not found in the portfolio.")

# Sell 90% of the token balance
# sell_amount = balance * 0.8
# sell_amount_raw = int(sell_amount * 10**decimals)
# decimals = int(portfolio_token['decimals'])
# sell_amount = float(balance) * 0.8  # Calculate 90% of the balance
# print(f"Selling {sell_amount} of token {portfolio_token['name']} ({portfolio_token['symbol']})")
# sell_amount_raw = int(sell_amount * 10**decimals)
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
import sys
from dotenv import load_dotenv
from moralis import sol_api

load_dotenv()
private_key = os.getenv('MY_BOT_WALLET_PRIVATE_KEY')
api_key = os.getenv("MORALIS_API_KEY")

if not private_key:
    raise ValueError("WALLET_PRIVATE_KEY not found in the .env file")

client = Client("https://api.mainnet-beta.solana.com")
sender = Keypair.from_base58_string(private_key)

wallet_address = '7Qq8RTV2ZP3niS1xmrvDf5PemARSJamWk3gVbECP3yaE'
file_path = f'./data/{wallet_address}_token_balances.json'

with open(file_path, 'r') as f:
    token_balances = json.load(f)

mint_address = sys.argv[1]

balance = None
decimals = None
portfolio_token = None

for token in token_balances:
    if token['mint'] == mint_address:
        balance = float(token['amount'])
        decimals = int(token['decimals'])
        portfolio_token = token
        break

if balance is None or decimals is None:
    raise ValueError(f"Mint address {mint_address} not found in the portfolio.")

print(f"Balance: {balance}")
print(f"Decimals: {decimals}")

sell_amount = float(balance) * 0.7
print(f"Selling 90% of balance: {sell_amount}")

sell_amount_raw = int(sell_amount * 10**decimals)
print(f"Sell amount raw: {sell_amount_raw}")

url = 'https://quote-api.jup.ag/v6/quote'
params = {
    'inputMint': mint_address,
    'outputMint': 'So11111111111111111111111111111111111111112',  # Converting to SOL
    'amount': sell_amount_raw,  # Sell all tokens
    'slippageBps': '300'  # 1% slippage
}
response = requests.get(url, params=params)
quoteResponse = response.json()
time.sleep(2)  # Small delay after fetching quote data
url = 'https://quote-api.jup.ag/v6/swap'
payload = {
    'userPublicKey': str(sender.pubkey()),
    'quoteResponse': quoteResponse,
}
response = requests.post(url, json=payload)
data = response.json()
swapTransaction = data['swapTransaction']
raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))
signature = sender.sign_message(message.to_bytes_versioned(raw_transaction.message))
signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])
opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)
transaction_id = json.loads(result.to_json())['result']
print('Transaction ID: ', transaction_id)


# # Prepare the request to Jupiter API to get a quote
# url = 'https://quote-api.jup.ag/v6/quote'
# params = {
#     'inputMint': mint_address,
#     'outputMint': 'So11111111111111111111111111111111111111112',  # Converting to SOL
#     'amount': sell_amount_raw,  # Sell 90% of tokens
#     'slippageBps': '200'  # 2% slippage
# }
# response = requests.get(url, params=params)
# quoteResponse = response.json()

# # Check if the quote was fetched correctly
# if 'routePlan' not in quoteResponse:
#     raise ValueError(f"Error fetching quote: {quoteResponse}")

# # Proceed with the swap if the quote is valid
# print(f"Received quote response: {quoteResponse}")

# # Small delay before the swap
# time.sleep(2)

# # Prepare the swap request to Jupiter API
# url = 'https://quote-api.jup.ag/v6/swap'
# payload = {
#     'userPublicKey': str(sender.pubkey()),
#     'quoteResponse': quoteResponse,
# }
# response = requests.post(url, json=payload)
# data = response.json()

# # Ensure valid swap response
# if 'swapTransaction' not in data:
#     raise ValueError(f"Error in swap: {data}")

# # Decode and sign the swap transaction
# swapTransaction = data['swapTransaction']
# raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))
# signature = sender.sign_message(message.to_bytes_versioned(raw_transaction.message))
# signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])

# # Send the signed transaction to the Solana network
# opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
# result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)


# # Fetch transaction result
# transaction_id = json.loads(result.to_json())['result']
# print('Transaction ID: ', transaction_id)

# # Delay between requests
# time.sleep(3)
