# Solana Token Bot

Here is the new section called **"Steps to Run Manually"**:

---

## Steps to Run Manually

Follow these steps to manually start the scripts and ensure that all processes are running correctly:

1. **Run `monitor_wallet.py` to create the initial wallet files**:
   - This step fetches your wallet's token balances and creates the required JSON files in the `wallets/` directory.
   - Command:
     ```bash
     python monitor_wallet.py
     ```

2. **Start `SCANNER.js` in a screen session**:
   - Use a screen session to run `SCANNER.js` continuously in the background. This script triggers the rug detection and token ranking process.
   - Commands:
     ```bash
     screen -S scanner
     node SCANNER.js
     ```
   - To detach from the screen session, press `Ctrl+A` followed by `D`.
   - To resume the session later, use:
     ```bash
     screen -r scanner
     ```

3. **Start the CRON job for `run_profit_monitor.sh`**:
   - Ensure that the `run_profit_monitor.sh` script is scheduled to run every minute via a Cron job. This script will trigger the `profit_monitor.py` script every 30 seconds.
   - Command:
     ```bash
     crontab -e
     ```
   - Add the following line if it's not already present to run the script every minute:
     ```bash
     * * * * * /path/to/run_profit_monitor.sh
     ```

After following these steps, the system will monitor your wallet, scan tokens for risks, and manage token buying and selling based on profit thresholds.

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
   - Sells 50% portion of tokens from the portfolio.
   - **Reads:** Token balance JSON from `./wallets/`.
   - **Creates:** Swap transaction results, logs.

- **monitor_wallet.py**  
   - Monitors the wallet and logs token buy prices.
   - **Reads:** Wallet balances, token data via API.
   - **Creates:** JSON files in `./data/`.

---

This setup allows you to monitor and trade tokens based on custom rankings and liquidity conditions on the Solana blockchain.
