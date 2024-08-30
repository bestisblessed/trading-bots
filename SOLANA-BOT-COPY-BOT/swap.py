# // if "added"
#     // buy token
# // else (removed)
#     // sell token

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
from moralis import sol_api

load_dotenv()
private_key = os.getenv('WALLET_PRIVATE_KEY')
api_key = os.getenv("MORALIS_API_KEY")

if not private_key:
    raise ValueError("WALLET_PRIVATE_KEY not found in the .env file")

client = Client("https://api.mainnet-beta.solana.com")
sender = Keypair.from_base58_string(private_key)

updates_path = './data/updated_tokens.json'

if os.path.exists(updates_path):
    with open(updates_path, 'r') as file:
        updated_tokens = json.load(file)

    for action, tokens in updated_tokens.items():
        for token in tokens:
            mint_address = token['mint']
            if action == 'added':
                print(f"Buying token with mint: {mint_address}")
                # Insert your buy logic here
                url = 'https://quote-api.jup.ag/v6/quote'
                params = {
                    'inputMint': 'So11111111111111111111111111111111111111112',
                    'outputMint': mint_address,
                    'amount': str(int(0.005 * 10**9)),  # Buy 0.005 eth of token
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



            elif action == 'removed':
                print(f"Selling token with mint: {mint_address}")

                # Fetch the portfolio balance
                params = {
                    "address": str(sender.pubkey()),  # Use the wallet address associated with the private key
                    "network": "mainnet",
                }

                result = sol_api.account.get_portfolio(api_key=api_key, params=params)

                # Find the specific token in the portfolio
                for portfolio_token in result.get('tokens', []):
                    if portfolio_token['mint'] == mint_address:
                        balance = portfolio_token['amount']

                        # Sell 90% instead
                        decimals = int(portfolio_token['decimals'])
                        sell_amount = float(balance) * 0.9  # Calculate 90% of the balance
                        print(f"Selling {sell_amount} of token {portfolio_token['name']} ({portfolio_token['symbol']})")
                        sell_amount_raw = int(sell_amount * 10**decimals)
                        # print(f"Token {portfolio_token['name']} ({portfolio_token['symbol']}) balance: {balance}")

                        # Selling the token
                        url = 'https://quote-api.jup.ag/v6/quote'
                        params = {
                            'inputMint': mint_address,
                            'outputMint': 'So11111111111111111111111111111111111111112',  # Converting to SOL
                            # 'amount': str(int(float(balance) * 10**int(portfolio_token['decimals']))),  # Sell all tokens
                            'amount': sell_amount_raw,  # Sell all tokens
                            'slippageBps': '100'  # 1% slippage
                        }
                        response = requests.get(url, params=params)
                        quoteResponse = response.json()

                        # Swap
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
                        break


    os.remove(updates_path)
    print('Processed and removed updated_tokens.json.')
else:
    print('No updated tokens found. Exiting...')