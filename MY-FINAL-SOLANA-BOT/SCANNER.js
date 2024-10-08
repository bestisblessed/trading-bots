// const { Connection, PublicKey } = require("@solana/web3.js");
// const { getMint } = require('@solana/spl-token');
// const fs = require('fs');
// const path = require('path');

// // Helper function to create a delay
// const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// const SESSION_HASH = 'QNDEMO' + Math.ceil(Math.random() * 1e9); // Random unique identifier for your session
// let credits = 0;

// const SOLANA_ENDPOINT = 'https://api.mainnet-beta.solana.com/';
// const raydium = new PublicKey('675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8');
// const connection = new Connection(SOLANA_ENDPOINT, {
//     wsEndpoint: SOLANA_ENDPOINT.replace('https://', 'wss://'),
//     httpHeaders: { "x-session-hash": SESSION_HASH }
// });

// // // Ensure the directory exists
// // const directory = './new_tokens';
// // if (!fs.existsSync(directory)) {
// //     fs.mkdirSync(directory, { recursive: true });
// // }

// // Monitor logs
// async function main(connection, programAddress) {
//     // console.log("Monitoring logs for program:", programAddress.toString());
//     console.log("");
//     console.log("Monitoring Solana Blockchain...");
//     console.log("");
//     connection.onLogs(
//         programAddress,
//         ({ logs, err, signature }) => {
//             if (err) return;

//             if (logs && logs.some(log => log.includes("initialize2"))) {
//                 // console.log("Signature for 'initialize2':", signature);
//                 fetchRaydiumAccounts(signature, connection);
//             }
//         },
//         "finalized"
//     );
// }

// // Parse transaction and filter data
// async function fetchRaydiumAccounts(txId, connection) {
//     const tx = await connection.getParsedTransaction(
//         txId,
//         {
//             maxSupportedTransactionVersion: 0,
//             commitment: 'confirmed'
//         });

//     credits += 100;

//     const accounts = tx?.transaction.message.instructions.find(ix => ix.programId.toBase58() === raydium.toBase58()).accounts;

//     if (!accounts) {
//         console.log("No accounts found in the transaction.");
//         return;
//     }

//     const tokenAIndex = 8;
//     const tokenBIndex = 9;

//     const tokenAAccount = accounts[tokenAIndex];
//     const tokenBAccount = accounts[tokenBIndex];

//     const tokenAAddress = tokenAAccount.toBase58();
//     const tokenBAddress = tokenBAccount.toBase58();

//     const token_address = tokenAAddress.startsWith("So1") ? tokenBAddress : tokenAAddress;

//     console.log(`Final Token Account Public Key: ${token_address}`);

//     // const newFileName = `${token_address}.json`;
//     // const newFilePath = path.join(directory, newFileName);

//     // const dataToSave = {
//     //     tokenAAddress,
//     //     tokenBAddress
//     // };

//     // fs.writeFileSync(newFilePath, JSON.stringify(dataToSave, null, 2));
//     // console.log(`Data saved to file: ${newFilePath}`);

//     // Fetch and print mint details
//     await fetchAndPrintMintDetails(token_address);
// }

// // Fetch mint details and print to the console
// async function fetchAndPrintMintDetails(mintAddress) {
//     try {
//         const mintPublicKey = new PublicKey(mintAddress);
//         const mintInfo = await getMint(connection, mintPublicKey);

//         // Calculate total supply adjusted for decimals
//         const totalSupply = Number(mintInfo.supply) / Math.pow(10, mintInfo.decimals);

//         // Prepare mint details
//         const mintDetails = {
//             mintAddress: mintAddress,
//             totalSupply: totalSupply,
//             decimals: mintInfo.decimals,
//             mintAuthority: mintInfo.mintAuthority ? mintInfo.mintAuthority.toBase58() : 'None',
//             freezeAuthority: mintInfo.freezeAuthority ? mintInfo.freezeAuthority.toBase58() : 'None',
//             isInitialized: mintInfo.isInitialized,
//         };

// //         console.log(`Mint Address: ${mintAddress}`);
// //         console.log(`Total Supply: ${Number(mintInfo.supply) / Math.pow(10, mintInfo.decimals)}`);
// //         console.log(`Decimals: ${mintInfo.decimals}`);
// //         console.log(`Mint Authority: ${mintInfo.mintAuthority ? mintInfo.mintAuthority.toBase58() : 'None'}`);
// //         console.log(`Freeze Authority: ${mintInfo.freezeAuthority ? mintInfo.freezeAuthority.toBase58() : 'None'}`);
// //         console.log(`Mint is Initialized: ${mintInfo.isInitialized}`);
// //         console.log('------------------------');
// //     } catch (error) {
// //         console.error(`Error fetching details for mint ${mintAddress}:`, error);
// //     }
// // }
//         // Print details to the console
//         console.log(`Mint Address: ${mintDetails.mintAddress}`);
//         console.log(`Total Supply: ${mintDetails.totalSupply}`);
//         console.log(`Decimals: ${mintDetails.decimals}`);
//         console.log(`Mint Authority: ${mintDetails.mintAuthority}`);
//         console.log(`Freeze Authority: ${mintDetails.freezeAuthority}`);
//         console.log(`Mint is Initialized: ${mintDetails.isInitialized}`);
//         // console.log('------------------------');

//         // Ensure the 'data' directory exists
//         const dataDirectory = './data';
//         if (!fs.existsSync(dataDirectory)) {
//             fs.mkdirSync(dataDirectory, { recursive: true });
//         }

//         // Define the file path
//         const fileName = `${mintAddress}.json`;
//         const filePath = path.join(dataDirectory, fileName);

//         // Save the mint details to the file
//         fs.writeFileSync(filePath, JSON.stringify(mintDetails, null, 2));

//         // Optional: Log that the data has been saved
//         console.log(`Mint details saved to file: ${filePath}`);
//         console.log('------------------------');
//         await delay(500);

//     } catch (error) {
//         console.error(`Error fetching details for mint ${mintAddress}:`, error);
//     }
// }

// main(connection, raydium).catch(console.error);
const { Connection, PublicKey } = require("@solana/web3.js");
const { getMint } = require('@solana/spl-token');
const fs = require('fs');
const path = require('path');

// Helper function to create a delay
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const SESSION_HASH = 'QNDEMO' + Math.ceil(Math.random() * 1e9); // Random unique identifier for your session
let credits = 0;

const SOLANA_ENDPOINT = 'https://api.mainnet-beta.solana.com/';
const raydium = new PublicKey('675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8');
const connection = new Connection(SOLANA_ENDPOINT, {
    wsEndpoint: SOLANA_ENDPOINT.replace('https://', 'wss://'),
    httpHeaders: { "x-session-hash": SESSION_HASH }
});

// Queue for processing transactions
const transactionQueue = [];
let isProcessingQueue = false;

// Monitor logs
async function main(connection, programAddress) {
    console.log("");
    console.log("Monitoring Solana Blockchain...");
    console.log("");
    connection.onLogs(
        programAddress,
        ({ logs, err, signature }) => {
            if (err) return;

            if (logs && logs.some(log => log.includes("initialize2"))) {
                // Enqueue the transaction signature for processing
                fetchRaydiumAccounts(signature, connection);
            }
        },
        "finalized"
    );
}

// Enqueue the transaction for processing
function fetchRaydiumAccounts(txId, connection) {
    transactionQueue.push({ txId, connection });
    processQueue();
}

// Process the queue sequentially
async function processQueue() {
    if (isProcessingQueue) return;
    isProcessingQueue = true;

    while (transactionQueue.length > 0) {
        const { txId, connection } = transactionQueue.shift();
        await processTransaction(txId, connection);
        // Delay between processing each transaction
        await delay(500); // Adjust the delay as needed
    }

    isProcessingQueue = false;
}

// Process each transaction
async function processTransaction(txId, connection) {
    try {
        const tx = await connection.getParsedTransaction(
            txId,
            {
                maxSupportedTransactionVersion: 0,
                commitment: 'confirmed'
            });

        credits += 100;

        const accounts = tx?.transaction.message.instructions.find(ix => ix.programId.toBase58() === raydium.toBase58()).accounts;

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

        // Fetch and print mint details
        await fetchAndPrintMintDetails(token_address);

    } catch (error) {
        console.error(`Error processing transaction ${txId}:`, error);
    }
}

// Fetch mint details and print to the console
async function fetchAndPrintMintDetails(mintAddress) {
    try {
        const mintPublicKey = new PublicKey(mintAddress);
        const mintInfo = await getMint(connection, mintPublicKey);

        // Calculate total supply adjusted for decimals
        const totalSupply = Number(mintInfo.supply) / Math.pow(10, mintInfo.decimals);

        // Prepare mint details
        const mintDetails = {
            mintAddress: mintAddress,
            totalSupply: totalSupply,
            decimals: mintInfo.decimals,
            mintAuthority: mintInfo.mintAuthority ? mintInfo.mintAuthority.toBase58() : 'None',
            freezeAuthority: mintInfo.freezeAuthority ? mintInfo.freezeAuthority.toBase58() : 'None',
            isInitialized: mintInfo.isInitialized,
        };

        // Print details to the console
        console.log(`Mint Address: ${mintDetails.mintAddress}`);
        console.log(`Total Supply: ${mintDetails.totalSupply}`);
        console.log(`Decimals: ${mintDetails.decimals}`);
        console.log(`Mint Authority: ${mintDetails.mintAuthority}`);
        console.log(`Freeze Authority: ${mintDetails.freezeAuthority}`);
        console.log(`Mint is Initialized: ${mintDetails.isInitialized}`);
        console.log('------------------------');

        // Ensure the 'data' directory exists
        const dataDirectory = './data';
        if (!fs.existsSync(dataDirectory)) {
            fs.mkdirSync(dataDirectory, { recursive: true });
        }

        // Define the file path
        const fileName = `${mintAddress}.json`;
        const filePath = path.join(dataDirectory, fileName);

        // Save the mint details to the file
        fs.writeFileSync(filePath, JSON.stringify(mintDetails, null, 2));

        // Optional: Log that the data has been saved
        // console.log(`Mint details saved to file: ${filePath}`);

        // Introduce a delay before processing the next token
        await delay(2000);

    } catch (error) {
        console.error(`Error fetching details for mint ${mintAddress}:`, error);
    }
}

main(connection, raydium).catch(console.error);