import os
import json

# Ensure the rankings directory exists
if not os.path.exists('./rankings/'):
    os.makedirs('./rankings/')

# Loop through each file in the rug-detections directory
for filename in os.listdir('./rug-detections/'):
    if filename.endswith('.json'):
        file_path = os.path.join('./rug-detections/', filename)
        
        # Open and read the token data
        with open(file_path, 'r') as f:
            token_data = json.load(f)
        
        # Initialize the rank
        rank = 0

        # Rule 1: If liquidity is under $999 - assign a score of 1
        if token_data['liquidity'] < 999:
            rank = 1
        
        # Rule 2: If it failed the mint authority or freeze authority check, assign a score of 1
        if token_data['mintAuthority'] != 'None' or token_data['freezeAuthority'] != 'None':
            rank = 1
        
        # Rule 3: If liquidity over $10,000 and 'PASS' the renounced ownership, assign a score of 4
        if token_data['liquidity'] > 10000 and token_data['ownershipRenounced']:
            rank = 4
        
        # Rule 4: If all tests pass, assign a score of 5
        if token_data['liquidity'] > 10000 and token_data['ownershipRenounced'] and \
           token_data['mintAuthority'] == 'None' and token_data['freezeAuthority'] == 'None':
            rank = 5

        # Save the rank in a new file
        output_filename = os.path.join('./rankings/', f"{token_data['tokenMintAddress']}_rank.json")
        rank_data = {
            'tokenMintAddress': token_data['tokenMintAddress'],
            'rank': rank
        }

        with open(output_filename, 'w') as outfile:
            json.dump(rank_data, outfile, indent=2)
        
        print(f"Processed {token_data['tokenMintAddress']} and assigned rank {rank}")
