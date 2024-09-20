import sys
import requests
import json

url = f"https://api.rugcheck.xyz/v1/stats/new_tokens"

# Send request to RugCheck API
response = requests.get(url, headers={"accept": "application/json"})

# Check for successful response
if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print(f"Error: {response.status_code}")
