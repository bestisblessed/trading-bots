import re
import solidity_parser
from solidity_parser import parser

def clean_contract_code(contract_code):
    """Remove non-Solidity content like headers or comments not part of the code."""
    # Remove any lines that are not part of Solidity code (like headers, metadata)
    cleaned_code = re.sub(r'^.*?:.*$', '', contract_code, flags=re.MULTILINE)
    return cleaned_code

def analyze_contract(contract_code):
    # Clean the contract code to remove any non-Solidity content
    cleaned_code = clean_contract_code(contract_code)
    
    # Parse the Solidity code
    parsed_contract = parser.parse(cleaned_code)
    
    # Initialize flags and storage for findings
    ownership_control_found = False
    restricted_transfers_found = False
    hidden_functions_found = False
    findings = []

    def check_ownership_control(node):
        """Check for ownership controls like onlyOwner."""
        nonlocal ownership_control_found
        if node.get('type') == 'FunctionDefinition':
            if node.get('modifiers'):
                for modifier in node['modifiers']:
                    if 'onlyOwner' in str(modifier):
                        ownership_control_found = True
                        findings.append(f"Ownership control found in function: {node['name']}")

    def check_transfer_restrictions(node):
        """Check for restricted transfers, particularly in transfer-related functions."""
        nonlocal restricted_transfers_found
        if node.get('type') == 'FunctionDefinition':
            if node.get('name') in ['transfer', 'transferFrom', '_transfer']:
                if 'require' in str(node):
                    restricted_transfers_found = True
                    findings.append(f"Transfer restrictions found in function: {node['name']}")

    def check_hidden_functions(node):
        """Check for functions that manipulate balances or restrict access."""
        nonlocal hidden_functions_found
        if node.get('type') == 'FunctionDefinition':
            if 'balance' in str(node) or 'transfer' in str(node):
                if 'onlyOwner' in str(node) or 'msg.sender' in str(node):
                    hidden_functions_found = True
                    findings.append(f"Potential hidden or restricted function found: {node['name']}")

    # Recursively traverse the parsed contract AST
    def traverse(node):
        check_ownership_control(node)
        check_transfer_restrictions(node)
        check_hidden_functions(node)

        for child in node.get('body', {}).get('statements', []):
            traverse(child)
    
    # Start traversing the AST
    for contract in parsed_contract['children']:
        traverse(contract)
    
    # Report findings
    if not findings:
        print("No significant findings detected.")
    else:
        for finding in findings:
            print(finding)

# Load and analyze a Solidity contract
contract_path = 'contracts/Erc20_0x9bEec80e62aA257cED8b0edD8692f79EE8783777.sol'
with open(contract_path, 'r') as contract_file:
    contract_code = contract_file.read()

analyze_contract(contract_code)
