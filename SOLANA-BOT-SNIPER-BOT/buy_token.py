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

# Load environment variables from .env file
load_dotenv()

# Get the private key from the .env file
private_key = os.getenv('MY_BOT_WALLET_PRIVATE_KEY')

if not private_key:
    raise ValueError("MY_BOT_WALLET_PRIVATE_KEY not found in the .env file")

client = Client("https://api.mainnet-beta.solana.com")
sender = Keypair.from_base58_string(private_key)

#quote
url = 'https://quote-api.jup.ag/v6/quote'
params = {
    'inputMint': 'So11111111111111111111111111111111111111112',
    'outputMint': '7nWspu6U3xW3y4uc9ffVi8PtKt4jvfHpCo8tRqsDpump',
    # 'amount': str(int(54000 * 10**6)), # Number of input tokens to sell
    'amount': str(int(0.005 * 10**9)), # Number of eth to swap
    'slippageBps': '150'  # 1% slippage
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

