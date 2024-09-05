
# Solana Trading Bot

## File Structure

- `SCANNER.js`: Node.js script that monitors the Solana blockchain for new Raydium token transactions and triggers a buy.
- `check_wallet_and_log_buy_prices.py`: Python script to check wallet token balances, fetch token prices, and log buy prices.
- `check_wallet_and_sell.py`: Python script to check token prices in the wallet and trigger sales based on price increases.
- `buy_token.py`: Python script to buy tokens when a new token transaction is detected.
- `sell_token_100.py`: Python script that sells tokens when the price increases by 75%.
- `sell_token_500.py`: Python script that sells tokens when the price increases by 500%.
- `data/`: Directory containing the token balances and buy prices in JSON format.

## Usage

### 1. Start the Scanner
Run the scanner to detect new tokens and automatically buy them:
```bash
node SCANNER.js
```

### 2. Log Buy Prices
After the scanner buys tokens, log the buy prices:
```bash
python check_wallet_and_log_buy_prices.py
```

### 3. Check Wallet and Trigger Sells
Monitor the token prices in your wallet and trigger sales if prices increase:
```bash
python check_wallet_and_sell.py
```

## License

This project is for personal use and educational purposes only.
