// require('dotenv').config();
// const { Connection, PublicKey } = require("@solana/web3.js");
// const fs = require('fs');
// const path = require('path');

// // Load environment variables
// console.log("Loading environment variables...");
// const RAYDIUM_PUBLIC_KEY = process.env.RAYDIUM_PUBLIC_KEY;
// const SOLANA_ENDPOINT = process.env.SOLANA_ENDPOINT;
// const SOLANA_ENDPOINT_TOKEN = process.env.SOLANA_ENDPOINT_TOKEN;
// console.log("Environment variables loaded.");

// const SESSION_HASH = 'QNDEMO' + Math.ceil(Math.random() * 1e9); // Random unique identifier for your session
// let credits = 0;

// console.log("Creating PublicKey object for Raydium...");
// const raydium = new PublicKey(RAYDIUM_PUBLIC_KEY);
// console.log("Raydium PublicKey created.");

// console.log("Establishing connection to Solana endpoint...");
// const connection = new Connection(SOLANA_ENDPOINT, {
//     wsEndpoint: SOLANA_ENDPOINT.replace('https://', 'wss://'),
//     httpHeaders: {
//         "x-session-hash": SESSION_HASH,
//         "Authorization": `Bearer ${SOLANA_ENDPOINT_TOKEN}`
//     }
// });
// console.log("Connection established.");

// // Ensure the directory exists
// console.log("Checking if directory exists...");
// const directory = './new_tokens';
// if (!fs.existsSync(directory)) {
//     console.log("Directory does not exist. Creating directory...");
//     fs.mkdirSync(directory, { recursive: true });
//     console.log("Directory created.");
// } else {
//     console.log("Directory already exists.");
// }

// // Monitor logs
// async function main(connection, programAddress) {
//     const chalk = (await import('chalk')).default;
//     console.log(chalk.blue("Monitoring logs for program:"), chalk.green(programAddress.toString()));

//     connection.onLogs(
//         programAddress,
//         ({ logs, err, signature }) => {
//             console.log("Log event received:", logs);
//             if (err) {
//                 console.error("Error in log event:", err);
//                 return;
//             }

//             if (logs.some(log => log.includes("initialize2"))) {
//                 console.log(chalk.yellow("Signature for 'initialize2':"), chalk.cyan(signature));
//                 fetchRaydiumAccounts(signature, connection);
//             }
//         },
//         "finalized"
//     );
//     console.log("Started log monitoring.");
// }

// // Parse transaction and filter data
// async function fetchRaydiumAccounts(txId, connection) {
//     const chalk = (await import('chalk')).default;
//     console.log("Fetching transaction data for ID:", txId);

//     try {
//         const tx = await connection.getParsedTransaction(
//             txId,
//             {
//                 maxSupportedTransactionVersion: 0,
//                 commitment: 'confirmed'
//             }
//         );

//         console.log("Transaction data fetched successfully.");

//         credits += 100;
//         console.log("Credits updated:", credits);

//         const accounts = tx?.transaction.message.instructions.find(ix => ix.programId.toBase58() === RAYDIUM_PUBLIC_KEY).accounts;

//         if (!accounts) {
//             console.log(chalk.red("No accounts found in the transaction."));
//             return;
//         }

//         const tokenAIndex = 8;
//         const tokenBIndex = 9;
        
//         const tokenAAccount = accounts[tokenAIndex];
//         const tokenBAccount = accounts[tokenBIndex];

//         const tokenAAddress = tokenAAccount.toBase58();
//         const tokenBAddress = tokenBAccount.toBase58();

//         const token_address = tokenAAddress.startsWith("So1") ? tokenBAddress : tokenAAddress;

//         console.log(chalk.magenta(`Transaction URL: https://solscan.io/tx/${txId}`));
//         console.log(chalk.blue(`Token A Account Public Key: ${tokenAAddress}`));
//         console.log(chalk.blue(`Token B Account Public Key: ${tokenBAddress}`));
//         console.log(chalk.blue(`Final Token Account Public Key: ${token_address}`));
//         console.log(chalk.yellow(`Total QuickNode Credits Used in this session: ${credits}`));

//         // Create the new file name and path
//         const newFileName = `${token_address}.json`;
//         const newFilePath = path.join(directory, newFileName);

//         // Prepare the data to be saved
//         const dataToSave = {
//             tokenAAddress,
//             tokenBAddress
//         };

//         console.log("Saving data to file:", newFilePath);
//         fs.writeFileSync(newFilePath, JSON.stringify(dataToSave, null, 2));
//         console.log(chalk.green(`Data saved to file: ${newFilePath}`));
//     } catch (error) {
//         console.error("Error fetching transaction data:", error);
//     }
// }

// console.log("Starting main function...");
// main(connection, raydium).catch(console.error);
// console.log("Main function execution started.");
require('dotenv').config();
const { Connection, PublicKey } = require("@solana/web3.js");
const fs = require('fs');
const path = require('path');
const chalk = require('chalk');

const RAYDIUM_PUBLIC_KEY = process.env.RAYDIUM_PUBLIC_KEY;
const SOLANA_ENDPOINT = process.env.SOLANA_ENDPOINT;
const SESSION_HASH = 'QNDEMO' + Math.ceil(Math.random() * 1e9); // Random unique identifier for your session
let credits = 0;

const raydium = new PublicKey(RAYDIUM_PUBLIC_KEY);
const connection = new Connection(SOLANA_ENDPOINT, 'confirmed');

// Ensure the directory exists
const directory = './new_tokens';
if (!fs.existsSync(directory)) {
    fs.mkdirSync(directory, { recursive: true });
}

// Monitor logs
async function main(connection, programAddress) {
    console.log(chalk.blue("Monitoring logs for program:"), chalk.green(programAddress.toString()));
    connection.onLogs(
        programAddress,
        ({ logs, err, signature }) => {
            if (err) return;

            if (logs && logs.some(log => log.includes("initialize2"))) {
                console.log(chalk.yellow("Signature for 'initialize2':"), chalk.cyan(signature));
                fetchRaydiumAccounts(signature, connection);
            }
        },
        "finalized"
    );
}

// Parse transaction and filter data
async function fetchRaydiumAccounts(txId, connection) {
    const tx = await connection.getParsedTransaction(txId, {
        maxSupportedTransactionVersion: 0,
        commitment: 'confirmed'
    });

    if (!tx) {
        console.log(chalk.red("Transaction not found."));
        return;
    }

    credits += 100;

    const instruction = tx.transaction.message.instructions.find(ix => ix.programId.toBase58() === RAYDIUM_PUBLIC_KEY);
    const accounts = instruction ? instruction.accounts : null;

    if (!accounts || accounts.length < 10) {
        console.log(chalk.red("No accounts or not enough accounts found in the transaction."));
        return;
    }

    const tokenAAccount = accounts[8];
    const tokenBAccount = accounts[9];

    const tokenAAddress = tokenAAccount.toBase58();
    const tokenBAddress = tokenBAccount.toBase58();

    const token_address = tokenAAddress.startsWith("So1") ? tokenBAddress : tokenAAddress;

    console.log(chalk.magenta(`Transaction URL: https://solscan.io/tx/${txId}`));
    console.log(chalk.blue(`Token A Account Public Key: ${tokenAAddress}`));
    console.log(chalk.blue(`Token B Account Public Key: ${tokenBAddress}`));
    console.log(chalk.blue(`Final Token Account Public Key: ${token_address}`));
    console.log(chalk.yellow(`Total QuickNode Credits Used in this session: ${credits}`));

    // Create the new file name and path
    const newFileName = `${token_address}.json`;
    const newFilePath = path.join(directory, newFileName);

    // Prepare the data to be saved
    const dataToSave = {
        tokenAAddress,
        tokenBAddress
    };

    // Save the data to the new file
    fs.writeFileSync(newFilePath, JSON.stringify(dataToSave, null, 2));

    console.log(chalk.green(`Data saved to file: ${newFilePath}`));
}

main(connection, raydium).catch(console.error);
