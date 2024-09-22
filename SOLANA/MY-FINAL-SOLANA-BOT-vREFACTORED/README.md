# Solana Token Bot

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
   - Sells 50% portion of tokens from the portfolio.
   - **Reads:** Token balance JSON from `./wallets/`.
   - **Creates:** Swap transaction results, logs.

- **monitor_wallet.py**  
   - Monitors the wallet and logs token buy prices.
   - **Reads:** Wallet balances, token data via API.
   - **Creates:** JSON files in `./data/`.

---

This setup allows you to monitor and trade tokens based on custom rankings and liquidity conditions on the Solana blockchain.
