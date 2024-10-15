import os
import requests
import base64
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
import time
import json
from solders.transaction import VersionedTransaction
from solders import message
from solana.rpc.types import TxOpts
from solana.rpc.commitment import Processed
from dotenv import load_dotenv
import sys
from moralis import sol_api
from colorama import init, Fore
import datetime
from solana.rpc.core import RPCException

# Initialize colorama
init(autoreset=True)

# Load environment variables from the .env file
load_dotenv()

# Get the API key and wallet address from the environment variables
api_key = os.getenv("MORALIS_API_KEY")
wallet_address = os.getenv("MY_BOT_WALLET_ADDRESS")
private_key = os.getenv('MY_BOT_KEY')

if not private_key:
    raise ValueError("MY_BOT_KEY not found in the .env file")
if not wallet_address:
    raise ValueError("MY_BOT_WALLET_ADDRESS not found in the .env file")

# Ensure the data directory exists
data_dir = 'wallets'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Define file paths
output_path = os.path.join(data_dir, f'{wallet_address}_token_balances.json')

# Fetch the portfolio balance using Moralis
params = {
    "address": wallet_address,
    "network": "mainnet",
}
result = sol_api.account.get_portfolio(api_key=api_key, params=params)

# Extract token balances from the portfolio
tokens = result.get('tokens', [])

# Save the current token balances to a JSON file
with open(output_path, 'w') as f:
    json.dump(tokens, f, indent=2)
print(f'Current token balances saved to {output_path}')

# List of token mint addresses to iterate over, with symbols commented
mint_addresses = [
    "7retgV8bwQtN6TL8GqJVGuuJ1EwLYBYYkR6cFzpc5pa5",  # Cristiano Ronaldo (RONALDO)
    "6eyxQYNxcmzKFYzoP7eNAqxmabAwyPyo3NjML97gJHAy",    # NVIDIA (NVIDIA)
    "ESVRQ6phc55VCw7sWB6JgW3PeTB6N68kvwjfsMPcpump",    # No1 tiktok frog (Omochi)
    "EE1JYjpo1croL7awdhu1PGys4WthumnWX5WT6uTDpump",    # Kaziwa (Kaziwa)
    "CFnREV96uczzbDGqvd8Fhhp9SPSkamy7Xwwk96xHZWjc",    # Mcoin (MCOIN)
    "EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm",    # dogwifhat ($WIF)
    "FnLaZCzTDVoooUXBV1QS5MXqGC5JRkeTsFpiGGyVhdKw",    # NVIDIA (NVIDIA)
    "2n6Yx3NJWSPAVwkEY3Ns8EgFHUZH6MNtKdwVgGvnEdkm",    # NO 1 Grand Theft Auto (GTA1)
    "G9athvtptL6DXLhJ4VwGJBdZUFZ9t7sgRwMW2iv5pump",    # WOOFIES (WOOFIES)
    "3cTSVhp4uRcwz59Cf8DuJeoPgjrwa8yqxY3564K1Qtr8",    # Pesto the Baby King Penguin (PESTO)
]

# Initialize the Solana client
client = Client("https://api.mainnet-beta.solana.com")
# Create the Keypair object from the private key
sender = Keypair.from_base58_string(private_key)

# Iterate over each mint address
for mint_address in mint_addresses:
    print(f"Processing token with mint address: {mint_address}")

    # Check if mint address is for a native SOL token
    if mint_address.startswith("So1"):
        print(Fore.RED + f"Skipping token with address starting with 'So1': {mint_address}")
        time.sleep(10)
        continue

    # Skip if the token is not in the portfolio
    token = next((token for token in tokens if token.get('mint') == mint_address), None)
    if not token:
        print(Fore.RED + f"Token with mint address {mint_address} not found in portfolio.")
        time.sleep(10)
        continue

    # Dexscreener API endpoint for Solana tokens
    dexscreener_api_endpoint = 'https://api.dexscreener.com/latest/dex/tokens'

    try:
        # Make API request to Dexscreener for the Solana token address
        response = requests.get(f'{dexscreener_api_endpoint}/{mint_address}')
        response.raise_for_status()  # Raise an exception for HTTP errors
        token_data = response.json()

        # Generate a timestamp for when the data is fetched
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Check if token data and pairs exist and are not None
        if token_data and 'pairs' in token_data and token_data['pairs']:
            print(Fore.WHITE + '-' * 50)
            print(Fore.CYAN + f"  TOKEN ADDRESS: {mint_address}")  # Print token address
            
            # Get the first pair only
            pair = token_data['pairs'][0]
            solana_token_name = pair['baseToken']['name']
            solana_token_symbol = pair['baseToken']['symbol']
            solana_token_liquidity = pair.get('liquidity', {}).get('base', 'Liquidity not available')
            quote_token_name = pair['quoteToken']['name']
            quote_token_symbol = pair['quoteToken']['symbol']
            quote_token_liquidity = pair.get('liquidity', {}).get('quote', 'Liquidity not available')
            usd_liquidity = pair.get('liquidity', {}).get('usd', 'USD liquidity not available')
            price_usd = pair.get('priceUsd', 'Price not available')  # Get token price in USD
            
            # Print liquidity and price details
            print(Fore.YELLOW + f"  {solana_token_name} ({solana_token_symbol}) / {quote_token_name} ({quote_token_symbol})")
            print(Fore.GREEN + f"  Price (USD): {price_usd}")
            print(Fore.GREEN + f"  Timestamp: {timestamp}")
            print(Fore.GREEN + f"  Liquidity (Solana Token): {solana_token_liquidity}")
            print(Fore.GREEN + f"  Liquidity (Quote Token): {quote_token_liquidity}")
            print(Fore.GREEN + f"  Liquidity (USD): {usd_liquidity}")
        else:
            print(Fore.WHITE + '-' * 50)
            print(Fore.RED + f"No liquidity pairs found for: {mint_address}")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching liquidity data for Solana token address: {mint_address}: {e}")

    # Load token balances from the file
    with open(output_path, 'r') as f:
        token_balances = json.load(f)

    # Find the token in the portfolio
    balance = None
    decimals = None
    for token in token_balances:
        if token['mint'] == mint_address:
            balance = float(token['amount'])
            decimals = int(token['decimals'])
            symbol = token.get('symbol', 'Unknown')  # Get the token symbol, default to 'Unknown'
            break

    # Raise an error if the token is not found
    if balance is None or decimals is None:
        print(Fore.RED + f"Mint address {mint_address} not found in the portfolio.")
        # time.sleep(10)
        continue

    print(f"Token Symbol: {symbol}")

    # Calculate the sell amount
    sell_amount = float(balance)  # Selling 100% of tokens
    print(f"Selling 100% of {symbol}: {sell_amount}")

    # Convert to raw token amount
    sell_amount_raw = int(sell_amount * 10**decimals)

    # Prepare the quote API request
    url = 'https://quote-api.jup.ag/v6/quote'
    params = {
        'inputMint': mint_address,
        'outputMint': 'So11111111111111111111111111111111111111112',  # Converting to SOL
        'amount': sell_amount_raw,  # Sell 100% of tokens
        'slippageBps': '600'  # 1% slippage
    }

    try:
        # Fetch the quote for the swap
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise error for failed requests
        quoteResponse = response.json()

        # Prepare the swap API request
        url = 'https://quote-api.jup.ag/v6/swap'
        payload = {
            'userPublicKey': str(sender.pubkey()),
            'quoteResponse': quoteResponse,
        }

        # Execute the swap
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise error for failed requests
        data = response.json()

        # Deserialize the swap transaction
        swapTransaction = data['swapTransaction']
        raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))

        # Sign the transaction
        signature = sender.sign_message(message.to_bytes_versioned(raw_transaction.message))
        signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])

        # Send the signed transaction
        opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
        result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)

        # Get the transaction ID
        transaction_id = json.loads(result.to_json())['result']
        print('Transaction ID: ', transaction_id)

    except RPCException as rpc_error:
        print(Fore.RED + f"Transaction failed with RPC error: {rpc_error}")
    except requests.exceptions.RequestException as req_error:
        print(Fore.RED + f"Request failed: {req_error}")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")

    # Sleep for 10 seconds after processing each token
    time.sleep(10)

print("Finished processing all tokens.")


Here are the clickable links to the Dexscreener pages for each token based on the provided mint addresses:

1. [Cristiano Ronaldo (RONALDO)](https://dexscreener.com/solana/7retgV8bwQtN6TL8GqJVGuuJ1EwLYBYYkR6cFzpc5pa5)
2. [Token Not Found](https://dexscreener.com/solana/DC6mPAuLkDYGM93p7VKUsS48MsJgNWgNzqspVbkk4WKh)
3. [BLEH GOAT (BLEH)](https://dexscreener.com/solana/ezk3nwHdpohYwukZiMCWgwEqqsnfBM7WL1xdmZ9pump)
4. [Solana The Rhino (SOLANA)](https://dexscreener.com/solana/81d1o6BfZeaF7GjqkKW3zk3fAUae6UZtT4Q4RGNDpump)
5. [Rock Head (ROAD)](https://dexscreener.com/solana/AaDVe74G8bp2t7SiBJCkHGM2qUEJg2Tp76yzcmnwxqB6)
6. [mould (MOULD)](https://dexscreener.com/solana/CCLFabhWgzg98PGuRvB8AFR2YfaktQrep58yMreypump)
7. [NVIDIA (NVIDIA)](https://dexscreener.com/solana/6eyxQYNxcmzKFYzoP7eNAqxmabAwyPyo3NjML97gJHAy)
8. [No1 tiktok frog (Omochi)](https://dexscreener.com/solana/ESVRQ6phc55VCw7sWB6JgW3PeTB6N68kvwjfsMPcpump)
9. [Kaziwa (Kaziwa)](https://dexscreener.com/solana/EE1JYjpo1croL7awdhu1PGys4WthumnWX5WT6uTDpump)
10. [Mcoin (MCOIN)](https://dexscreener.com/solana/CFnREV96uczzbDGqvd8Fhhp9SPSkamy7Xwwk96xHZWjc)
11. [Chao Chor (ChaoChor)](https://dexscreener.com/solana/CPCd7iEztRBCsJoyPhC2yArnx5EH8MqxbC4jXJCqpump)
12. [dogwifhat ($WIF)](https://dexscreener.com/solana/EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm)
13. [NVIDIA (NVIDIA)](https://dexscreener.com/solana/FnLaZCzTDVoooUXBV1QS5MXqGC5JRkeTsFpiGGyVhdKw)
14. [NO 1 Grand Theft Auto (GTA1)](https://dexscreener.com/solana/2n6Yx3NJWSPAVwkEY3Ns8EgFHUZH6MNtKdwVgGvnEdkm)
15. [WOOFIES (WOOFIES)](https://dexscreener.com/solana/G9athvtptL6DXLhJ4VwGJBdZUFZ9t7sgRwMW2iv5pump)
16. [Pesto the Baby King Penguin (PESTO)](https://dexscreener.com/solana/3cTSVhp4uRcwz59Cf8DuJeoPgjrwa8yqxY3564K1Qtr8)
17. [RUBOTS($ RUBOTS)](https://dexscreener.com/solana/HRctWzuVxtDM8a9mzd91AJNYCYa2w5qrgnEvaJb1pump)
18. [it is nothing. (nope)](https://dexscreener.com/solana/9RxQeMi2MRjiFU2ZfPWirP8M242KMhoyW9SB1UvfVXhu)
19. [MUU DENG (MUU)](https://dexscreener.com/solana/Ax9aDQGKDTSGFxaHyefWAcu5AfG8cUAaxmshhzLtpump)
20. [EZO The Flying Squirrel (EZO)](https://dexscreener.com/solana/AzN2kJgSpkK5TXz9cg8MKWYgr27xaQ1N71oRGRj2pump)

You can click the links to view each token's details on Dexscreener. If there's anything more you need, just let me know!