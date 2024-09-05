
# SOLANA-BOT-SNIPER-BOT-FINAL

This project contains scripts to monitor Solana wallet token balances, log their buy prices, and perform token selling based on price changes.

## Features

1. **Token Balance Logging (`check_wallet_and_log_buy_prices.py`)**:
   - Fetches the current token balances for a specified Solana wallet.
   - Logs buy prices and liquidity details for each token in `buy_prices.json`.
   
2. **Token Sell Logic (`check_wallet_and_sell.py`)**:
   - Fetches the current prices of tokens in the wallet.
   - Checks if the token price has increased and triggers a sell action if a specified price threshold is met.

## Requirements

The following packages are required to run the scripts:

```bash
requests==2.31.0
solders==0.21.0
solana==0.34.3
python-dotenv==1.0.1
moralis==0.1.49
```

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-repo/solana-bot-sniper-bot-final.git
   cd solana-bot-sniper-bot-final
   ```

2. **Set up Python environment:**

   Create and activate a virtual environment (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the project root with the following content:

   ```
   MY_BOT_WALLET_PRIVATE_KEY=<your_private_key>
   ```

   Replace `<your_private_key>` with the private key for the wallet you want to use.

## Usage

### 1. Log Token Balances and Buy Prices

This script fetches the current token balances and logs their buy prices.

```bash
python check_wallet_and_log_buy_prices.py
```

### 2. Check Prices and Trigger Sells

This script checks the price changes for tokens in the wallet and triggers a sell if the price increases by a set threshold.

```bash
python check_wallet_and_sell.py
```

## File Structure

- `check_wallet_and_log_buy_prices.py`: Logs token balances and buy prices.
- `check_wallet_and_sell.py`: Checks token prices and sells based on price changes.
- `buy_prices.json`: Stores the buy prices and liquidity information for each token.
- `.env`: Stores environment variables like your wallet private key.

## License

This project is licensed under the MIT License.
