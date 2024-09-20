import requests

# url = "https://api.rugcheck.xyz/v1/tokens/FEN72JRg6uxbE4sXVJa4kJCWgvEBA5yqeQ1iCu1Npump/report/summary"
# url = "https://api.rugcheck.xyz/v1/tokens/AfuHBzLSiTFiiMZgp9eExPtnHG2ZcqWqMQjGgpgfBXLw/report/summary"
# url = "https://api.rugcheck.xyz/v1/tokens/2TVjXHnvRJ9mFS8K9jKQE7ThYjm6NQvh5f66ijECjaUE/report/summary"
url = "https://api.rugcheck.xyz/v1/tokens/Ag19bdRfrDU4WprGrbN8pJaEP3YbLvbuC9gsnaoJgFKz/report/summary"
response = requests.get(url, headers={"accept": "application/json"})
if response.status_code == 200:
    print(response.json())  # Print the JSON response
else:
    print(f"Error: {response.status_code}")
