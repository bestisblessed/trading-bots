"""
Steps Breakdown:
Setup:

Connect to the Base network using web3.py.
Set your MetaMask wallet's private key and contract details securely.
Transaction Details:

Specify the amount of ETH you wish to use to buy $BRETT tokens (amount_in_wei).
The path array defines the swap route from WETH to $BRETT. The WETH address used in the script needs to be the correct WETH address on the Base network.
Build and Send Transaction:

The transaction is constructed with parameters like gas limit, gas price, and nonce.
The transaction is signed using your private key and then broadcast to the network.
Monitor Transaction:

The script waits for the transaction to be mined and prints the transaction hash upon success.
Important Notes:
ABI: You'll need the ABI of the Uniswap/DEX router to interact with the contract properly. This is usually available on Etherscan or provided by the contract developer.
Gas and Fees: Ensure the gas limit and gas price are appropriate for the transaction. Adjust as needed based on current network conditions.
Security: Keep your private key secure, preferably using environment variables or other secure storage mechanisms.
This script will allow you to programmatically buy 5 $BRETT tokens using your MetaMask wallet on the Base network. Adjust the amount_in_wei and path as necessary to meet your needs.
"""

from web3 import Web3
from eth_account import Account
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to the Base network RPC
base_rpc_url = "https://base-mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
web3 = Web3(Web3.HTTPProvider(base_rpc_url))

# Ensure the connection is established
if not web3.isConnected():
    print("Failed to connect to the Base network")
    exit()

# Your MetaMask private key and address
private_key = os.getenv('PRIVATE_KEY')  # Securely store your private key in a .env file
wallet_address = web3.eth.account.privateKeyToAccount(private_key).address

# Contract details
brett_contract_address = "0x532f27101965dd16442E59d40670FaF5eBB142E4"
amount_to_buy = 5  # The number of $BRETT tokens you want to buy

# ABI of the Uniswap or BaseSwap Router contract
router_abi = [
    # Include the ABI of the Router contract, typically obtained from Etherscan or the contract's developer
]

# Initialize contract instance
router_contract = web3.eth.contract(address="0x2626664c2603336E57B271c5C0b26F421741e481", abi=router_abi)

# Set up the transaction to swap ETH for BRETT tokens
amount_in_wei = web3.toWei(0.01, 'ether')  # Replace 0.01 with the amount of ETH you want to spend
path = [
    web3.toChecksumAddress("0xC9E4d95Bf11FdBdEB0FCE7a62c1bC7954E15f5E9"),  # WETH contract address (wrapped ETH)
    web3.toChecksumAddress(brett_contract_address)
]

# Build the transaction
txn = router_contract.functions.swapExactETHForTokens(
    0,  # Minimum amount of tokens to receive, set to 0 for this example
    path,  # Path: WETH -> $BRETT
    wallet_address,  # Your wallet address to receive $BRETT
    (int(web3.eth.getBlock('latest').timestamp) + 10000)  # Deadline: current time + buffer
).buildTransaction({
    'from': wallet_address,
    'value': amount_in_wei,  # The amount of ETH to swap
    'gas': 200000,
    'gasPrice': web3.toWei('5', 'gwei'),
    'nonce': web3.eth.getTransactionCount(wallet_address),
    'chainId': 8453  # Base chain ID
})

# Sign the transaction
signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)

# Send the transaction
txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

# Wait for the transaction to be mined
receipt = web3.eth.waitForTransactionReceipt(txn_hash)
print(f'Transaction successful with hash: {txn_hash.hex()}')
