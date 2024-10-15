import sys
import requests
import json

# Ensure the mint address is provided as an argument
if len(sys.argv) > 1:
    tokenMintAddress = sys.argv[1]
    url = f"https://api.rugcheck.xyz/v1/tokens/{tokenMintAddress}/report/summary"

    # Send request to RugCheck API
    response = requests.get(url, headers={"accept": "application/json"})

    # Check for successful response
    if response.status_code == 200:
        # Save the JSON response to a file in the 'rug-detections' folder
        result = response.json()
        print(result)
        output_file = f'./rug-detections/{tokenMintAddress}.json'
        with open(output_file, 'w') as file:
            json.dump(result, file, indent=4)
        print(f"RugCheck Result saved to {output_file}")
    else:
        print(f"Error: {response.status_code}")
else:
    print("Please provide a token mint address.")
print('------------------------')

# import sys
# import requests
# import json
# import os
# from solana.publickey import PublicKey
# from solana.rpc.api import Client

# # Ensure the directory exists for saving results
# output_directory = './rug-detections/'
# if not os.path.exists(output_directory):
#     os.makedirs(output_directory)

# # Function to fetch and analyze the token
# def rugDetector(tokenMintAddress):
#     # Simulate token analysis result (replace this with actual logic)
#     result = {
#         'tokenMintAddress': tokenMintAddress,
#         'analysis': {
#             'risk_score': 100,  # Example risk score
#             'liquidity': 5000,  # Example liquidity value
#             'holder_concentration': 'High',
#             'is_freezable': False
#         }
#     }

#     # Save the result to a JSON file
#     file_path = os.path.join(output_directory, f'{tokenMintAddress}.json')
#     with open(file_path, 'w') as json_file:
#         json.dump(result, json_file, indent=4)

#     print(f'Saved analysis for token {tokenMintAddress} to {file_path}')

# # Get the token mint address passed as an argument
# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         tokenMintAddress = sys.argv[1]
#         rugDetector(tokenMintAddress)
#     else:
#         print("Please provide a token mint address.")
