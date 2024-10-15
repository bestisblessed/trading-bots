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
# from moralis import sol_api
# import time

# # Load environment variables
# load_dotenv()
# private_key = os.getenv('MY_BOT_WALLET_PRIVATE_KEY')
# api_key = os.getenv("MORALIS_API_KEY")

# # Ensure private key is loaded
# if not private_key:
#     raise ValueError("WALLET_PRIVATE_KEY not found in the .env file")

# # Initialize Solana client
# client = Client("https://api.mainnet-beta.solana.com")
# sender = Keypair.from_base58_string(private_key)

# def sell_token(mint_address):
#     # Fetch the portfolio balance using Moralis API
#     params = {
#         "address": str(sender.pubkey()),  # Use the wallet address associated with the private key
#         "network": "mainnet",
#     }
    
#     result = sol_api.account.get_portfolio(api_key=api_key, params=params)

#     # Find the specific token in the portfolio
#     for portfolio_token in result.get('tokens', []):
#         if portfolio_token['mint'] == mint_address:
#             balance = portfolio_token['amount']
#             decimals = int(portfolio_token['decimals'])
#             sell_amount = float(balance) * 0.9  # Sell 90% of the balance
#             sell_amount_raw = int(sell_amount * 10**decimals)

#             print(f"Selling {sell_amount} of token {portfolio_token['name']} ({portfolio_token['symbol']})")

#             # Prepare the quote for selling the token into SOL
#             url = 'https://quote-api.jup.ag/v6/quote'
#             params = {
#                 'inputMint': mint_address,
#                 'outputMint': 'So11111111111111111111111111111111111111112',  # Converting to SOL
#                 'amount': sell_amount_raw,  # Sell 90% of the tokens
#                 'slippageBps': '200'  # 2% slippage
#             }

#             response = requests.get(url, params=params)
#             quoteResponse = response.json()

#             # Small delay after fetching quote data
#             time.sleep(2)

#             # Execute the swap transaction
#             url = 'https://quote-api.jup.ag/v6/swap'
#             payload = {
#                 'userPublicKey': str(sender.pubkey()),
#                 'quoteResponse': quoteResponse,
#             }
#             response = requests.post(url, json=payload)
#             data = response.json()
#             swapTransaction = data['swapTransaction']

#             # Sign and send the transaction
#             raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))
#             signature = sender.sign_message(message.to_bytes_versioned(raw_transaction.message))
#             signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])

#             opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
#             result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)

#             # Get the transaction ID
#             transaction_id = json.loads(result.to_json())['result']
#             print('Transaction ID: ', transaction_id)
#             break
#     else:
#         print(f"Token with mint address {mint_address} not found in the portfolio.")

# # Input: mint address of the token to sell
# mint_address_input = '5YzQjNqUfQ87m38xejJsUy35b8DsihYvN2ajinMjfmfh'
# sell_token(mint_address_input)
import json
import os
import sys
import requests, base64
from solders.keypair import Keypair
from solana.rpc.api import Client
from solana.rpc.commitment import Processed
from solders.transaction import VersionedTransaction
from solders import message
from solana.rpc.types import TxOpts
from dotenv import load_dotenv
from moralis import sol_api
import time

# Load environment variables
load_dotenv()
private_key = os.getenv('MY_BOT_WALLET_PRIVATE_KEY')
api_key = os.getenv("MORALIS_API_KEY")

# Ensure private key is loaded
if not private_key:
    raise ValueError("WALLET_PRIVATE_KEY not found in the .env file")

# Initialize Solana client
client = Client("https://api.mainnet-beta.solana.com")
sender = Keypair.from_base58_string(private_key)

def sell_token(mint_address):
    # Fetch the portfolio balance using Moralis API
    params = {
        "address": str(sender.pubkey()),  # Use the wallet address associated with the private key
        "network": "mainnet",
    }
    
    result = sol_api.account.get_portfolio(api_key=api_key, params=params)

    # Find the specific token in the portfolio
    for portfolio_token in result.get('tokens', []):
        if portfolio_token['mint'] == mint_address:
            balance = portfolio_token['amount']
            decimals = int(portfolio_token['decimals'])
            sell_amount = float(balance) * 0.9  # Sell 90% of the balance
            sell_amount_raw = int(sell_amount * 10**decimals)

            print(f"Selling {sell_amount} of token {portfolio_token['name']} ({portfolio_token['symbol']})")

            # Prepare the quote for selling the token into SOL
            url = 'https://quote-api.jup.ag/v6/quote'
            params = {
                'inputMint': mint_address,
                'outputMint': 'So11111111111111111111111111111111111111112',  # Converting to SOL
                'amount': sell_amount_raw,  # Sell 90% of the tokens
                'slippageBps': '200'  # 2% slippage
            }

            response = requests.get(url, params=params)
            quoteResponse = response.json()

            # Small delay after fetching quote data
            time.sleep(2)

            # Execute the swap transaction
            url = 'https://quote-api.jup.ag/v6/swap'
            payload = {
                'userPublicKey': str(sender.pubkey()),
                'quoteResponse': quoteResponse,
            }
            response = requests.post(url, json=payload)
            data = response.json()
            swapTransaction = data['swapTransaction']

            # Sign and send the transaction
            raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))
            signature = sender.sign_message(message.to_bytes_versioned(raw_transaction.message))
            signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])

            opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
            result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)

            # Get the transaction ID
            transaction_id = json.loads(result.to_json())['result']
            print('Transaction ID: ', transaction_id)
            break
    else:
        print(f"Token with mint address {mint_address} not found in the portfolio.")

# Ensure mint address is passed as an argument
if len(sys.argv) < 2:
    print("Usage: python script.py <mint_address>")
    sys.exit(1)

# Get the mint address from the first argument
mint_address_input = sys.argv[1]
sell_token(mint_address_input)
