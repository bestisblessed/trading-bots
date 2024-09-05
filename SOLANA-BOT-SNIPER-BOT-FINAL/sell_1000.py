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

sell_amount = float(balance) * 0.9
print(f"Selling the rest of balance: {sell_amount}")

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
