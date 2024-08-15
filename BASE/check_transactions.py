import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import pytz

load_dotenv()
api_key = os.getenv('BASESCAN_API_KEY')

contract_address = '0x9bEec80e62aA257cED8b0edD8692f79EE8783777'   # Replace with the token contract address

# def check_transactions(token_address, api_key, high_value_threshold=1e6, suspicious_activity_threshold=5):
#     """
#     Check for suspicious transactions for a given token address.

#     Parameters:
#     - token_address (str): The contract address of the token to check.
#     - api_key (str): The API key for accessing the blockchain explorer.
#     - high_value_threshold (float): The value threshold to flag high-value transactions.
#     - suspicious_activity_threshold (int): The number of suspicious transactions to trigger a warning.

#     Returns:
#     - dict: A summary of the findings, including a count of suspicious transactions and any high-value transactions detected.
#     """
#     basescan_api_endpoint = 'https://api.basescan.org/api'
#     params = {
#         'module': 'account',
#         'action': 'tokentx',
#         'address': token_address,
#         'sort': 'desc',
#         'apikey': api_key
#     }
    
#     try:
#         response = requests.get(basescan_api_endpoint, params=params)
#         response.raise_for_status()
#         data = response.json()
        
#         if data['status'] == '1':
#             transactions = data['result']
#             suspicious_transactions = []
#             high_value_transactions = []

#             for tx in transactions:
#                 tx_value = float(tx['value']) / (10 ** int(tx['tokenDecimal']))  # Convert value to human-readable format
#                 if tx_value >= high_value_threshold:
#                     high_value_transactions.append({
#                         'tx_hash': tx['hash'],
#                         'value': tx_value,
#                         'timestamp': tx['timeStamp']
#                     })
#                 if tx_value > 0:  # Any non-zero value transaction can be considered for suspicious activity
#                     suspicious_transactions.append({
#                         'tx_hash': tx['hash'],
#                         'value': tx_value,
#                         'timestamp': tx['timeStamp']
#                     })
            
#             # Filter suspicious transactions to those exceeding the threshold
#             if len(suspicious_transactions) >= suspicious_activity_threshold:
#                 print(f"Warning: Detected {len(suspicious_transactions)} suspicious transactions.")
#             else:
#                 print("No significant suspicious activity detected.")

#             if high_value_transactions:
#                 print(f"High-value transactions detected:")
#                 for tx in high_value_transactions:
#                     print(f"  Transaction Hash: {tx['tx_hash']}")
#                     print(f"  Value: ${tx['value']}")
#                     print(f"  Timestamp: {tx['timestamp']}")
#             else:
#                 print("No high-value transactions detected.")

#             return {
#                 'suspicious_transactions_count': len(suspicious_transactions),
#                 'high_value_transactions': high_value_transactions
#             }
#         else:
#             print(f"Error: {data['message']}")
#             return None
#     except requests.exceptions.RequestException as e:
#         print(f"Request error: {e}")
#         return None

# results = check_transactions(token_address, api_key)
# print(results)
def convert_timestamp(timestamp):
    """Convert Unix timestamp to human-readable format using timezone-aware datetime."""
    dt = datetime.fromtimestamp(int(timestamp), pytz.UTC)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def check_transactions(contract_address, api_key, high_value_threshold=1e6, suspicious_activity_threshold=5):
    """
    Check for suspicious transactions and total buys and sells for a given token address.

    Parameters:
    - contract_address (str): The contract address of the token to check.
    - api_key (str): The API key for accessing the blockchain explorer.
    - high_value_threshold (float): The value threshold to flag high-value transactions.
    - suspicious_activity_threshold (int): The number of suspicious transactions to trigger a warning.

    Returns:
    - dict: A summary of the findings, including a count of suspicious transactions, total buys, total sells, and any high-value transactions detected.
    """
    basescan_api_endpoint = 'https://api.basescan.org/api'
    params = {
        'module': 'account',
        'action': 'tokentx',
        'address': contract_address,
        'sort': 'desc',
        'apikey': api_key
    }
    
    try:
        response = requests.get(basescan_api_endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] == '1':
            transactions = data['result']
            suspicious_transactions = []
            high_value_transactions = []
            address_transactions = {}
            total_buys = 0
            total_sells = 0

            for tx in transactions:
                tx_value = float(tx['value']) / (10 ** int(tx['tokenDecimal']))  # Convert value to human-readable format
                timestamp = convert_timestamp(tx['timeStamp'])
                
                if tx_value >= high_value_threshold:
                    high_value_transactions.append({
                        'tx_hash': tx['hash'],
                        'value': tx_value,
                        'timestamp': timestamp,
                        'from': tx['from'],
                        'to': tx['to']
                    })
                
                # Track transactions per address
                if tx['from'] not in address_transactions:
                    address_transactions[tx['from']] = []
                if tx['to'] not in address_transactions:
                    address_transactions[tx['to']] = []
                
                address_transactions[tx['from']].append(tx_value)
                address_transactions[tx['to']].append(tx_value)

                if tx_value > 0:  # Any non-zero value transaction can be considered for suspicious activity
                    suspicious_transactions.append({
                        'tx_hash': tx['hash'],
                        'value': tx_value,
                        'timestamp': timestamp,
                        'from': tx['from'],
                        'to': tx['to']
                    })

                # Determine if it's a buy or sell
                if tx['to'].lower() == contract_address.lower():  # Buying tokens
                    total_buys += 1
                if tx['from'].lower() == contract_address.lower():  # Selling tokens
                    total_sells += 1

            # Analyze suspicious activity
            suspicious_activity = []
            for address, tx_values in address_transactions.items():
                total_value = sum(tx_values)
                if len(tx_values) > 10 and total_value > high_value_threshold:  # Arbitrary values for demonstration
                    suspicious_activity.append({
                        'address': address,
                        'total_value': total_value,
                        'transaction_count': len(tx_values)
                    })

            if len(suspicious_transactions) >= suspicious_activity_threshold:
                print(f"Warning: Detected {len(suspicious_transactions)} suspicious transactions.")
                for activity in suspicious_activity:
                    print(f"  Address: {activity['address']}")
                    print(f"  Total Value: ${activity['total_value']}")
                    print(f"  Number of Transactions: {activity['transaction_count']}")
            else:
                print("No significant suspicious activity detected.")

            if high_value_transactions:
                print(f"High-value transactions detected:")
                for tx in high_value_transactions:
                    print(f"  Transaction Hash: {tx['tx_hash']}")
                    print(f"  Value: ${tx['value']}")
                    print(f"  Timestamp: {tx['timestamp']}")
                    print(f"  From: {tx['from']}")
                    print(f"  To: {tx['to']}")
            else:
                print("No high-value transactions detected.")

            print(f"Total Buy Transactions: {total_buys}")
            print(f"Total Sell Transactions: {total_sells}")

            return {
                'suspicious_transactions_count': len(suspicious_transactions),
                'high_value_transactions': high_value_transactions,
                'suspicious_activity': suspicious_activity,
                'total_buys': total_buys,
                'total_sells': total_sells
            }
        else:
            print(f"Error: {data['message']}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

results = check_transactions(contract_address, api_key)
print(results)