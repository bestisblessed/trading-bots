import requests

# Hardcoded API URL with the token ID included
url = "https://api.rugcheck.xyz/v1/tokens/Ag19bdRfrDU4WprGrbN8pJaEP3YbLvbuC9gsnaoJgFKz/lockers"

# Send GET request
response = requests.get(url, headers={"accept": "application/json"})

# Check for successful response
if response.status_code == 200:
    print("Lockers Information:")
    print(response.json())
else:
    print(f"Error: {response.status_code}")
