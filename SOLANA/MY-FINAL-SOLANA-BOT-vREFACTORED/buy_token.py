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

# Load environment variables from .env file
load_dotenv()

# Get the private key from the .env file
private_key = os.getenv('MY_BOT_KEY')

if not private_key:
    raise ValueError("MY_BOT_KEY not found in the .env file")

client = Client("https://api.mainnet-beta.solana.com")
sender = Keypair.from_base58_string(private_key)

# Get the token address (outputMint) from the command-line argument
if len(sys.argv) < 2:
    raise ValueError("Output token address (mint) required as an argument")
output_mint = sys.argv[1]

#quote
url = 'https://quote-api.jup.ag/v6/quote'
params = {
    'inputMint': 'So11111111111111111111111111111111111111112',
    'outputMint': output_mint,
    'amount': str(int(0.002 * 10**9)), # Number of SOL to swap
    'slippageBps': '300'  # 3% slippage
}
response = requests.get(url, params=params)
quoteResponse = response.json()

#swap
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
result_raw_output = json.loads(result.to_json())
transaction_id = json.loads(result.to_json())['result']
print(result_raw_output)
print('Transaction ID: ', transaction_id)