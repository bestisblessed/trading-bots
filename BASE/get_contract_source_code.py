import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import pytz
from colorama import Fore, Style 

load_dotenv()
api_key = os.getenv('BASESCAN_API_KEY')  # Example, not used in this script but might be needed for other APIs

contract_address = '0x9bEec80e62aA257cED8b0edD8692f79EE8783777' 

def get_contract_source_code(contract_address):
    """
    Get the Solidity source code of a verified smart contract from BaseScan.

    Parameters:
    - contract_address (str): The address of the verified contract.

    Returns:
    - dict: The source code details including the Solidity code.
    """
    base_url = 'https://api.basescan.org/api'
    params = {
        'module': 'contract',
        'action': 'getsourcecode',
        'address': contract_address,
        'apikey': api_key
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        result = response.json()

        if result['status'] == '1':
            # Extract source code information
            source_code_info = result['result'][0]
            contract_name = source_code_info.get('ContractName', 'N/A')
            compiler_version = source_code_info.get('CompilerVersion', 'N/A')
            source_code = source_code_info.get('SourceCode', 'N/A')

            print(f"Contract Address: {contract_address}")
            print(f"Contract Name: {contract_name}")
            print(f"Compiler Version: {compiler_version}")
            # print(f"Source Code: {source_code[:500]}...")

            # Construct the filename
            filename = f"./contracts/{contract_name}_{contract_address}.sol"

            # Save the source code and details to a file
            with open(filename, 'w') as file:
                file.write(f"Contract Address: {contract_address}\n")
                file.write(f"Contract Name: {contract_name}\n")
                file.write(f"Compiler Version: {compiler_version}\n\n")
                file.write(f"Source Code:\n{source_code}\n")

            print(Fore.GREEN + f"Source code saved to {filename}" + Style.RESET_ALL)

            return {
                'contract_address': contract_address,
                'contract_name': contract_name,
                'compiler_version': compiler_version,
                'source_code': source_code
            }
        else:
            print(f"Error: {result['message']}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

source_code_info = get_contract_source_code(contract_address)


