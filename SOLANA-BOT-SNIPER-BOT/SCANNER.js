const { Connection, PublicKey } = require("@solana/web3.js");
const fs = require('fs');
const path = require('path');

// Use Solana public RPC endpoint (Mainnet)
const SOLANA_ENDPOINT = "https://api.mainnet-beta.solana.com";
const connection = new Connection(SOLANA_ENDPOINT, "confirmed");

const SESSION_HASH = 'QNDEMO' + Math.ceil(Math.random() * 1e9);
let credits = 0;

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
                console.log("Signature for 'initialize2':", signature);
                await fetchRaydiumAccounts(signature, connection);
            }
        },
        "finalized" // Commitment level for confirmed transactions
    );
}

// // Fetch and process transaction with a 0.5s delay on 429 error
// async function fetchRaydiumAccounts(txId, connection, retryCount = 0) {
//     const maxRetries = 5;
//     const baseDelay = 500;  // 0.25-second delay

//     try {
//         // Fetch the transaction data
//         const tx = await connection.getParsedTransaction(
//             txId,
//             {
//                 maxSupportedTransactionVersion: 0,
//                 commitment: 'finalized'
//             });

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

//         // console.log(`Transaction URL: https://solscan.io/tx/${txId}`);
//         // console.log(`Token A Account Public Key: ${tokenAAddress}`);
//         // console.log(`Token B Account Public Key: ${tokenBAddress}`);
//         console.log(`Final Token Account Public Key: ${token_address}`);
//         // console.log(`Total RPC Credits Used in this session: ${credits}`);

//         // Save the token data to a JSON file
//         const newFileName = `${token_address}.json`;
//         const newFilePath = path.join(directory, newFileName);

//         const dataToSave = {
//             tokenAAddress,
//             tokenBAddress
//         };

//         fs.writeFileSync(newFilePath, JSON.stringify(dataToSave, null, 2));

//         console.log(`Data saved to file: ${newFilePath}`);
//     } catch (error) {
//         if (error.response && error.response.status === 429 && retryCount < maxRetries) {
//             const delay = baseDelay * Math.pow(2, retryCount);  // Exponential backoff
//             console.log(`Server responded with 429. Retrying after ${delay}ms...`);
//             await new Promise(resolve => setTimeout(resolve, delay));  // Wait before retrying
//             return fetchRaydiumAccounts(txId, connection, retryCount + 1);  // Retry after delay
//         } else {
//             console.error("Error fetching Raydium accounts:", error);
//         }
//     }
// }
const { exec } = require('child_process'); // For running the Python swap script

async function fetchRaydiumAccounts(txId, connection, retryCount = 0) {
    const maxRetries = 5;
    const baseDelay = 500;  // 0.25-second delay

    try {
        // Fetch the transaction data
        const tx = await connection.getParsedTransaction(
            txId,
            {
                maxSupportedTransactionVersion: 0,
                commitment: 'finalized'
            });

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

        // Save the token data to a JSON file
        const newFileName = `${token_address}.json`;
        const newFilePath = path.join(directory, newFileName);

        const dataToSave = {
            tokenAAddress,
            tokenBAddress
        };

        fs.writeFileSync(newFilePath, JSON.stringify(dataToSave, null, 2));

        console.log(`Data saved to file: ${newFilePath}`);

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
            console.log(`Swap stdout: ${stdout}`);
        });

    } catch (error) {
        if (error.response && error.response.status === 429 && retryCount < maxRetries) {
            const delay = baseDelay * Math.pow(2, retryCount);  // Exponential backoff
            console.log(`Server responded with 429. Retrying after ${delay}ms...`);
            await new Promise(resolve => setTimeout(resolve, delay));  // Wait before retrying
            return fetchRaydiumAccounts(txId, connection, retryCount + 1);  // Retry after delay
        } else {
            console.error("Error fetching Raydium accounts:", error);
        }
    }
}



// Start monitoring logs
main(connection, raydium).catch(console.error);
