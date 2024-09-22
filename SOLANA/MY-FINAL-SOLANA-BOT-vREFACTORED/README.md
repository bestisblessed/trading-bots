Here’s a simple README for your bot:

---

# Solana Token Bot

This bot allows you to detect and rank tokens using the Solana blockchain, trigger specific actions like buying tokens based on rankings, and analyze token liquidity.

## Running the Bot

To run the bot, follow these steps:

1. **Install Node.js**  
   Make sure you have Node.js installed on your system. You can download and install it from [Node.js official site](https://nodejs.org).

2. **Install Python**  
   Make sure you have Python 3 installed on your system. You can download and install it from [Python official site](https://www.python.org).

3. **Install Dependencies**
   - Install required Python libraries using `pip`:
     ```
     pip install -r requirements.txt
     ```
   - Install Node.js packages (if any are required):
     ```
     npm install
     ```

4. **Configure Environment Variables**  
   Create a `.env` file in the project directory with the following environment variables:
   ```
   MY_BOT_KEY=<your-private-key>
   MY_BOT_WALLET_ADDRESS=<your-wallet-address>
   MORALIS_API_KEY=<your-moralis-api-key>
   ```

5. **Run the Bot**  
   Run the bot using the `SCANNER.js` script:
   ```
   node SCANNER.js
   ```

---

## Script Overview

Here is a list of each script, what it does, and the files it reads or creates:

- **SCANNER.js**  
   - Main script that triggers the rug detection and rankings process for Solana tokens.
   - **Reads:** Token data, CSV, and JSON files from `./rug-detections/`.
   - **Creates:** Token ranking files in `./rankings/`.

- **1_rug_detector_final.py**  
   - Detects rug pulls and token liquidity issues. Skips tokens with low liquidity or bad rankings.
   - **Reads:** Solana token data, `./rug-detections/*.csv`.
   - **Creates:** JSON results in `./rug-detections/` and updates token data.

- **2_rug_detector_final.js**  
   - Generates rankings for tokens based on liquidity and ownership information. Triggers additional analysis and processes.
   - **Reads:** JSON files from `./rug-detections/`.
   - **Creates:** Ranking files in `./rankings/`.

- **buy_token.py**  
   - Buys tokens with good rankings (rank 3, 4, or 5). Executes a swap using Solana's token swap API.
   - **Reads:** Token information from command line or files.
   - **Creates:** Buy transaction results, logs in the console, updates JSON files.

- **sell_token.py**  
   - Sells a portion of tokens from the portfolio.
   - **Reads:** Token balance JSON from `./wallets/`.
   - **Creates:** Swap transaction results, logs.

- **monitor_wallet.py**  
   - Monitors the wallet and logs token buy prices.
   - **Reads:** Wallet balances, token data via API.
   - **Creates:** JSON files in `./data/`.

- **check_wallet_and_log_buy_prices.py**  
   - Fetches wallet data and logs prices of tokens in the portfolio.
   - **Reads:** Solana wallet, token data.
   - **Creates:** Buy prices log in `./data/buy_prices.json`.

---

This setup allows you to monitor and trade tokens based on custom rankings and liquidity conditions on the Solana blockchain.
