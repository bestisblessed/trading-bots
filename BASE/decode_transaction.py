from web3 import Web3

# Connect to an Ethereum node
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))

# Sample transaction data
transaction_data = {
    "blockHash": "0xca5e0e49574052c3a1e667c33bf9a70cbfc645bfba28ecefa251ea640753729a",
    "blockNumber": "0x10a5415",
    "from": "0xd72c6421a6b9bc0d673fb3863c303e4cdc3148c4",
    "gas": "0xcd41f",
    "gasPrice": "0x911446",
    "hash": "0x0a3efb6fdb90bb1d7b7a2fd450eb0e9a4a461122886808eba0adaa21909c08ee",
    "input": "0x2cd42262000000000000000000000000000000000000000000000000000000000000a984...",
    "nonce": "0x0",
    "to": "0x0bf8edd756ff6caf3f583d67a9fd8b237e40f58a",
    "transactionIndex": "0x54",
    "value": "0xa8dc487e2ca000",
    "type": "0x2"
}

# Decode the input data
def decode_input(input_data):
    try:
        method_signature = input_data[:10]  # First 4 bytes + 0x prefix
        function_abi = w3.eth.contract().get_function_by_selector(method_signature)
        decoded_input = w3.eth.contract().decode_function_input(input_data)
        return function_abi, decoded_input
    except:
        return None, None

# Analyze the transaction
def analyze_transaction(transaction):
    input_data = transaction.get('input', '')
    function_abi, decoded_input = decode_input(input_data)

    if function_abi:
        print(f"Method being called: {function_abi.function_identifier}")
        print(f"Decoded input: {decoded_input}")

        # Check for buy/sell functions
        if function_abi.function_identifier in ['buy', 'swapExactETHForTokens', 'swapETHForExactTokens']:
            print("This is likely a buy transaction.")
        elif function_abi.function_identifier in ['sell', 'swapExactTokensForETH', 'swapTokensForExactETH']:
            print("This is likely a sell transaction.")
        else:
            print("The method does not match common buy/sell functions.")
    else:
        print("Unable to decode the input data.")

# Run the analysis
analyze_transaction(transaction_data)
