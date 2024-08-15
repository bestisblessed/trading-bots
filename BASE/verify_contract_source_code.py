# import re
# import requests
# from dotenv import load_dotenv
# import os

# load_dotenv()
# api_key = os.getenv('BASESCAN_API_KEY')

# def fetch_source_code(contract_address, api_key):
#     url = 'https://api.basescan.org/api'
#     params = {
#         'module': 'contract',
#         'action': 'getsourcecode',
#         'address': contract_address,
#         'apikey': api_key
#     }
#     response = requests.get(url, params=params)
#     data = response.json()
#     if data['status'] == '1':
#         source_code = data['result'][0]['SourceCode']
#         return source_code
#     else:
#         raise Exception(f"Error fetching source code: {data['message']}")

# def analyze_source_code(source_code):
#     # Simple checks for malicious patterns
#     checks = {
#         'blacklist': re.search(r'blacklist', source_code, re.IGNORECASE) is not None,
#         'hidden_functions': re.search(r'function\s+[^\s]+\s*\(.*\)\s*{', source_code) is not None,
#         'owner_privileges': re.search(r'onlyOwner', source_code, re.IGNORECASE) is not None,
#         'dangerous_functions': re.search(r'withdraw|transfer|approve', source_code, re.IGNORECASE) is not None,
#     }

#     results = []
#     for key, value in checks.items():
#         if value:
#             results.append(f"Potential issue found: {key.replace('_', ' ').capitalize()}")
    
#     return results

# def main():
#     contract_address = '0x9bEec80e62aA257cED8b0edD8692f79EE8783777'  # Replace with actual contract address
#     try:
#         source_code = fetch_source_code(contract_address, api_key)
#         issues = analyze_source_code(source_code)
#         if issues:
#             print("Potential scam indicators found:")
#             for issue in issues:
#                 print(f"- {issue}")
#         else:
#             print("No obvious scam indicators found.")
#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     main()










# v2
import os

def analyze_contract(file_path):
    """Analyze the Solidity contract for potential issues."""
    with open(file_path, 'r') as file:
        source_code = file.read()

    # Basic checks for common scam indicators
    issues = []

    # Check for owner privileges
    if 'onlyOwner' in source_code or 'owner()' in source_code:
        issues.append('Contract has owner privileges functions.')

    # Check for transfer restrictions
    if 'require' in source_code and ('transfer' in source_code or 'transferFrom' in source_code):
        issues.append('Contract may restrict token transfers.')

    # Check for suspicious patterns
    suspicious_patterns = ['selfdestruct', 'kill', 'destroy', 'emergencyStop', 'revert']
    if any(pattern in source_code for pattern in suspicious_patterns):
        issues.append('Contract contains potentially dangerous patterns.')

    if not issues:
        return 'No issues detected.'
    
    return issues

# Directory containing Solidity contract files
contracts_dir = './contracts/'

if not os.path.exists(contracts_dir):
    print(f"Directory {contracts_dir} does not exist.")
else:
    for filename in os.listdir(contracts_dir):
        if filename.endswith('.sol'):
            file_path = os.path.join(contracts_dir, filename)
            print(f"Analyzing contract file: {filename}")
            result = analyze_contract(file_path)
            print(f"Result for {filename}: {result}\n")










# v3
import os
import re

def analyze_contract(file_path):
    """
    Analyzes a Solidity smart contract for potential scam indicators.

    Args:
        file_path (str): Path to the Solidity contract file.

    Returns:
        list: A list of detected issues with the contract.
    """
    issues = []
    
    with open(file_path, 'r') as file:
        source_code = file.read()
    
    # Check for ownership-related functions and modifiers
    if re.search(r'\b(owner|onlyOwner|transferOwnership)\b', source_code, re.IGNORECASE):
        issues.append('Contract has owner privileges functions.')
    
    # Check for transfer restrictions
    if re.search(r'\b(restrict|block|require|onlyOwner)\b.*\b(transfer|send)\b', source_code, re.IGNORECASE):
        issues.append('Contract may restrict token transfers.')
    
    # Check for common dangerous patterns
    if re.search(r'\b(transferFrom|approve)\b.*\b(onlyOwner|onlyContract)\b', source_code, re.IGNORECASE):
        issues.append('Contract contains potentially dangerous patterns.')
    
    # Detailed checks for more sophisticated scam indicators
    if re.search(r'\b(address(.*)(\=\s*0x0)|balance(.*)(<|<=|>\s*0))\b', source_code, re.IGNORECASE):
        issues.append('Contract may contain suspicious address or balance checks.')

    return issues

# Example usage
contract_file = 'contracts/Erc20_0x9bEec80e62aA257cED8b0edD8692f79EE8783777.sol'
result = analyze_contract(contract_file)
print(f'Result for {contract_file}: {result}')
