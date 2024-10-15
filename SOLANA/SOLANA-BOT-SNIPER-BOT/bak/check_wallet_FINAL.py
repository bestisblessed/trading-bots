import os
import json
from dotenv import load_dotenv
from moralis import sol_api

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv("MORALIS_API_KEY")

# Define the parameters with the Solana wallet address and network
params = {
    "address": "6ZDdVLFc2CRaPUwUGnfUsmXr32EBWoNaM9Axf5LWUjc6",
    "network": "mainnet",
}

# Fetch the portfolio balance
result = sol_api.account.get_portfolio(
    api_key=api_key,
    params=params,
)

# Extract token balances
tokens = result.get('tokens', [])

# Ensure the data/ directory exists
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Define the path for the output file
wallet_address = params['address']
output_path = os.path.join(data_dir, f'{wallet_address}_token_balances.json')
updates_path = os.path.join(data_dir, 'updated_tokens.json')

# Load previous balances if they exist
previous_data = []
if os.path.exists(output_path):
    with open(output_path, 'r') as f:
        previous_data = json.load(f)

# Compare previous and current data
previous_mints = set(token['mint'] for token in previous_data)
current_mints = set(token.get('mint', 'Unknown') for token in tokens)

added_tokens = [token for token in tokens if token.get('mint', 'Unknown') not in previous_mints]
removed_tokens = [token for token in previous_data if token['mint'] not in current_mints]

# Log changes
if added_tokens or removed_tokens:
    updated_tokens = {
        'added': added_tokens,
        'removed': removed_tokens,
    }
    
    # Log added tokens
    if added_tokens:
        print('\nNEW TOKENS ADDED:')
        for token in added_tokens:
            print(f"  Token: {token.get('name', 'Unknown')} ({token.get('symbol', 'Unknown')})")
            print(f"  Mint: {token.get('mint', 'Unknown')}")
            print(f"  Amount: {token.get('amount', '0')}\n")
    
    # Log removed tokens
    if removed_tokens:
        print('\nTOKENS REMOVED:')
        for token in removed_tokens:
            print(f"  Token: {token['name']} ({token['symbol']})")
            print(f"  Mint: {token['mint']}")
            print(f"  Amount: {token['amount']}\n")

    # Save the updated tokens to a separate JSON file
    with open(updates_path, 'w') as f:
        json.dump(updated_tokens, f, indent=2)
    print(f'Updated tokens saved to {updates_path}')

# Save the current token balances to a JSON file
with open(output_path, 'w') as f:
    json.dump(tokens, f, indent=2)
print(f'Current token balances saved to {output_path}')

# Print the native SOL balance
native_balance = result.get('nativeBalance', {})
print(f"SOL Balance: {native_balance.get('solana', '0')} SOL")

# Print the token balances in a more organized format
print("\nToken Balances:")
for token in tokens:
    name = token.get('name', 'Unknown')
    symbol = token.get('symbol', 'Unknown')
    amount = token.get('amount', '0')
    amount_raw = token.get('amountRaw')
    mint = token.get('mint', 'Unknown')
    associated_token_address = token.get('associatedTokenAddress')
    print(f"Token: {name} ({symbol})")
    print(f"  Mint Address: {mint}")
    print(f"  Associated Token Address: {associated_token_address}")
    print(f"  Balance: {amount}")
    print(f"  Balance Raw: {amount_raw}\n")