const { Connection, PublicKey } = require("@solana/web3.js");
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

// Use Solana public RPC endpoint (Mainnet)
const SOLANA_ENDPOINT = "https://api.mainnet-beta.solana.com";
const connection = new Connection(SOLANA_ENDPOINT, "confirmed");

const SESSION_HASH = 'QNDEMO' + Math.ceil(Math.random() * 1e9);
let credits = 0;
let isPriceCheckerRunning = false;

const raydium = new PublicKey('675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8');

// Ensure the directory exists
const directory = './new_tokens';
if (!fs.existsSync(directory)) {
    fs.mkdirSync(directory, { recursive: true });
}

// Monitor logs with efficient filtering
async function main(connection, programAddress) {
    console.log("Monitoring logs for program:", programAddress.toString());

    connection.onLogs(
        programAddress,
        async ({ logs, err, signature }) => {
            if (err) return;

            // Only process logs that contain "initialize2"
            if (logs && logs.some(log => log.includes("initialize2"))) {
                // console.log("Signature for 'initialize2':", signature);
                await fetchRaydiumAccounts(signature, connection);
            }
        },
        "finalized" // Commitment level for confirmed transactions
    );
}

// async function fetchRaydiumAccounts(txId, connection, retryCount = 0) {
//     const maxRetries = 5;
//     const baseDelay = 250;  // 0.25-second delay

//     try {
//         const tx = await connection.getParsedTransaction(
//             txId,
//             { maxSupportedTransactionVersion: 0, commitment: 'finalized' }
//         );

//         credits += 100;

//         const accounts = tx?.transaction.message.instructions.find(ix => ix.programId.toBase58() === raydium.toBase58())?.accounts;
//         if (!accounts) {
//             console.log("No accounts found in the transaction.");
//             return;
//         }

//         const tokenAIndex = 8;
//         const tokenBIndex = 9;
//         const tokenAAccount = accounts[tokenAIndex];
//         const tokenBAccount = accounts[tokenBIndex];

//         const tokenAAddress = tokenAAccount.toBase58();
//         const tokenBAddress = tokenBAccount.toBase58();
//         const token_address = tokenAAddress.startsWith("So1") ? tokenBAddress : tokenAAddress;

//         console.log(`Final Token Account Public Key: ${token_address}`);

//         if (token_address.endsWith("pump")) {
//             // Save the token data to a JSON file
//             const newFileName = `${token_address}.json`;
//             const newFilePath = path.join(directory, newFileName);
//             const dataToSave = { tokenAAddress, tokenBAddress };
        
//             fs.writeFileSync(newFilePath, JSON.stringify(dataToSave, null, 2));
//             console.log(`Data saved to file: ${newFilePath}`);
        
//             // Delay before executing the Python scripts
//             console.log("Running buy_token.py");
//             await new Promise(resolve => setTimeout(resolve, 3000)); // 3 seconds delay
        
//             // Call the Python swap script with the new token_address
//             const swapCommand = `python buy_token.py ${token_address}`;
//             exec(swapCommand, (error, stdout, stderr) => {
//                 if (error) {
//                     console.error(`Error executing swap: ${error.message}`);
//                     return;
//                 }
//                 if (stderr) {
//                     console.error(`Swap stderr: ${stderr}`);
//                     return;
//                 }
//                 console.log(`Done buy_token.py: ${stdout}`);
//             });
        
//             // Delay before executing the next Python script
//             console.log("Running check_wallet_and_log_buy_prices.py");
//             await new Promise(resolve => setTimeout(resolve, 3000)); // 3 seconds delay
        
//             // Call the next Python script to log buy price and token details
//             const checkWalletCommand = `python check_wallet_and_log_buy_prices.py`;
//             exec(checkWalletCommand, (error, stdout, stderr) => {
//                 if (error) {
//                     console.error(`Error executing check_wallet_and_log_buy_prices.py: ${error.message}`);
//                     return;
//                 }
//                 if (stderr) {
//                     console.error(`check_wallet_and_log_buy_prices.py stderr: ${stderr}`);
//                     return;
//                 }
//                 console.log(`Done check_wallet_and_log_buy_prices.py: ${stdout}`);
//             });
//         } else {
//             console.log(`Token address ${token_address} does not end with 'pump'. Skipping swap and logging.`);
//         }
//     }
// }
async function fetchRaydiumAccounts(txId, connection, retryCount = 0) {
    const maxRetries = 5;
    const baseDelay = 250;  // 0.25-second delay

    try {
        const tx = await connection.getParsedTransaction(
            txId,
            { maxSupportedTransactionVersion: 0, commitment: 'finalized' }
        );

        credits += 100;

        const accounts = tx?.transaction.message.instructions.find(ix => ix.programId.toBase58() === raydium.toBase58())?.accounts;
        if (!accounts) {
            console.log("No accounts found in the transaction.");
            return;
        }

        const tokenAIndex = 8;
        const tokenBIndex = 9;
        const tokenAAccount = accounts[tokenAIndex];
        const tokenBAccount = accounts[tokenBIndex];

        const tokenAAddress = tokenAAccount.toBase58();
        const tokenBAddress = tokenBAccount.toBase58();
        const token_address = tokenAAddress.startsWith("So1") ? tokenBAddress : tokenAAddress;

        console.log(`Final Token Account Public Key: ${token_address}`);

        if (token_address.endsWith("pump")) {
            // Save the token data to a JSON file
            const newFileName = `${token_address}.json`;
            const newFilePath = path.join(directory, newFileName);
            const dataToSave = { tokenAAddress, tokenBAddress };
        
            fs.writeFileSync(newFilePath, JSON.stringify(dataToSave, null, 2));
            console.log(`Data saved to file: ${newFilePath}`);
        
            // Delay before executing the Python scripts
            console.log("Running buy_token.py");
            await new Promise(resolve => setTimeout(resolve, 3000)); // 3 seconds delay
        
            // Call the Python swap script with the new token_address
            const swapCommand = `python buy_token.py ${token_address}`;
            exec(swapCommand, (error, stdout, stderr) => {
                if (error) {
                    console.error(`Error executing swap: ${error.message}`);
                    return;
                }
                if (stderr) {
                    console.error(`Swap stderr: ${stderr}`);
                    return;
                }
                console.log(`Done buy_token.py: ${stdout}`);
            });
        
            // Delay before executing the next Python script
            console.log("Running check_wallet_and_log_buy_prices.py");
            await new Promise(resolve => setTimeout(resolve, 3000)); // 3 seconds delay
        
            // Call the next Python script to log buy price and token details
            const checkWalletCommand = `python check_wallet_and_log_buy_prices.py`;
            exec(checkWalletCommand, (error, stdout, stderr) => {
                if (error) {
                    console.error(`Error executing check_wallet_and_log_buy_prices.py: ${error.message}`);
                    return;
                }
                if (stderr) {
                    console.error(`check_wallet_and_log_buy_prices.py stderr: ${stderr}`);
                    return;
                }
                console.log(`Done check_wallet_and_log_buy_prices.py: ${stdout}`);
            });
        } else {
            console.log(`Token address ${token_address} does not end with 'pump'. Skipping swap and logging.`);
        }
    } catch (error) { // Add this catch block to handle errors
        if (error.response && error.response.status === 429 && retryCount < maxRetries) {
            const delay = baseDelay * Math.pow(2, retryCount);  // Exponential backoff
            console.log(`Server responded with 429. Retrying after ${delay}ms...`);
            await new Promise(resolve => setTimeout(resolve, delay));
            return fetchRaydiumAccounts(txId, connection, retryCount + 1);
        } else {
            console.error("Error fetching Raydium accounts:", error);
        }
    }
}

function runPythonPriceChecker() {
    if (!isPriceCheckerRunning) {
        isPriceCheckerRunning = true;
        // const priceCheckerCommand = `FORCE_COLOR=1 python check_wallet_and_sell.py`;
        const priceCheckerCommand = `python check_wallet_and_sell.py`;
        exec(priceCheckerCommand, (error, stdout, stderr) => {
            isPriceCheckerRunning = false;
            if (error) {
                console.error(`Error executing check_wallet_and_sell.py: ${error.message}`);
                return;
            }
            if (stderr) {
                console.error(`check_wallet_and_sell.py stderr: ${stderr}`);
                return;
            }
            // console.log(`Checking %'s gained..`);
            // console.log(`check_wallet_and_sell.py stdout: ${stdout}`);
            console.log(`${stdout}`);
            // console.log('Done check_wallet_and_sell.py')
        });
    }
}

// Run the Python price checker every 5 seconds
function startPriceChecker() {
    setInterval(runPythonPriceChecker, 5000);
}

// Start monitoring logs and the price checker concurrently
main(connection, raydium).catch(console.error);
startPriceChecker();
