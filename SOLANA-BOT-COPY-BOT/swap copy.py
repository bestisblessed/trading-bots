# // if "added"
#     // buy token
# // else (removed)
#     // sell token

import json
import os

updates_path = './data/updated_tokens.json'

if os.path.exists(updates_path):
    with open(updates_path, 'r') as file:
        updated_tokens = json.load(file)

    for action, tokens in updated_tokens.items():
        for token in tokens:
            if action == 'added':
                print(f"Buying token with mint: {token['mint']}")
                # Insert your buy logic here




            elif action == 'removed':
                print(f"Selling token with mint: {token['mint']}")
                # Insert your sell logic here



    os.remove(updates_path)
    print('Processed and removed updated_tokens.json.')
else:
    print('No updated tokens found. Exiting...')