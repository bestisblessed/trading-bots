// // require('dotenv').config();
// const { Connection, PublicKey } = require("@solana/web3.js");
// const fs = require('fs');
// const path = require('path');

// // const RAYDIUM_PUBLIC_KEY = process.env.RAYDIUM_PUBLIC_KEY;
// // const SOLANA_ENDPOINT = process.env.SOLANA_ENDPOINT;
// const SESSION_HASH = 'QNDEMO' + Math.ceil(Math.random() * 1e9); // Random unique identifier for your session
// let credits = 0;

// // const SOLANA_ENDPOINT = 'https://tiniest-burned-mansion.solana-mainnet.quiknode.pro/a5f42fa1b144c8f334deb792e7567894965b96b0';
// const SOLANA_ENDPOINT = 'https://fabled-misty-putty.solana-mainnet.quiknode.pro/d6c562f9b1106b60e01c276a42c58a1c182298c4/';

// const raydium = new PublicKey('675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8');
// const connection = new Connection(SOLANA_ENDPOINT, {
//     wsEndpoint: SOLANA_ENDPOINT.replace('https://', 'wss://'),
//     httpHeaders: {"x-session-hash": SESSION_HASH}
// });

// // Ensure the directory exists
// const directory = './new_tokens';
// if (!fs.existsSync(directory)) {
//     fs.mkdirSync(directory, { recursive: true });
// }

// // Polling interval (1 second)
// const POLLING_INTERVAL = 1000;

// // Keep track of the last processed signature
// let lastProcessedSignature = null;

// // Monitor logs with optimized filtering through polling
// async function main(connection, programAddress) {
//     console.log("Monitoring logs for program:", programAddress.toString());
    
//     // Poll logs every second
//     setInterval(async () => {
//         try {
//             // Get the latest transaction signatures from the Raydium program
//             const logs = await connection.getConfirmedSignaturesForAddress2(
//                 programAddress,
//                 { limit: 1 }
//             );
            
//             // If we have new signatures, process them
//             if (logs && logs.length > 0) {
//                 const latestSignature = logs[0].signature;
                
//                 // Check if the latest signature is new
//                 if (latestSignature !== lastProcessedSignature) {
//                     // console.log("New signature found:", latestSignature);
//                     await fetchRaydiumAccounts(latestSignature, connection);
//                     lastProcessedSignature = latestSignature;
//                 }
//             }
//         } catch (error) {
//             console.error("Error fetching signatures:", error);
//         }
//     }, POLLING_INTERVAL);
// }
// // // Monitor logs for specific keyword "initialize2"
// // async function main(connection, programAddress) {
// //     console.log("Monitoring logs for program:", programAddress.toString());

// //     // Set up a log subscription for the given program
// //     connection.onLogs(
// //         programAddress,
// //         ({ logs, err, signature }) => {
// //             if (err) {
// //                 // console.error("Error in logs:", err);
// //                 return;
// //             }

// //             // Check if the logs contain the "initialize2" keyword
// //             if (logs && logs.some(log => log.includes("initialize2"))) {
// //                 // console.log("Signature for 'initialize2':", signature);
// //                 fetchRaydiumAccounts(signature, connection);  // Call fetchRaydiumAccounts for the matching signature
// //             } else {
// //                 // console.log("No 'initialize2' found in logs for signature:", signature);
// //             }
// //         },
// //         "finalized"  // Commitment level for confirmed transactions
// //     );
// // }


// // Parse transaction and filter data with optimized usage
// async function fetchRaydiumAccounts(txId, connection) {
//     try {
//         // Fetch the transaction data more selectively
//         const tx = await connection.getParsedTransaction(
//             txId,
//             {
//                 maxSupportedTransactionVersion: 0,
//                 commitment: 'finalized' // Use 'finalized' to ensure you're fetching less often
//             });

//         credits += 100;

//         const accounts = tx?.transaction.message.instructions.find(ix => ix.programId.toBase58() === raydium.toBase58())?.accounts;

//         if (!accounts) {
//             // console.log("No accounts found in the transaction.");
//             return;
//         }

//         const tokenAIndex = 8;
//         const tokenBIndex = 9;

//         const tokenAAccount = accounts[tokenAIndex];
//         const tokenBAccount = accounts[tokenBIndex];

//         const tokenAAddress = tokenAAccount.toBase58();
//         const tokenBAddress = tokenBAccount.toBase58();

//         // // Check if tokenBAddress does not start with "So1"
//         // if (!tokenBAddress.startsWith("So1")) {
//         //     console.log("No new coin");
//         //     return;  // Exit the function early
//         // }

//         const token_address = tokenAAddress.startsWith("So1") ? tokenBAddress : tokenAAddress;

//         console.log(`Transaction URL: https://solscan.io/tx/${txId}`);
//         console.log(`Token A Account Public Key: ${tokenAAddress}`);
//         console.log(`Token B Account Public Key: ${tokenBAddress}`);
//         console.log(`Final Token Account Public Key: ${token_address}`);
//         console.log(`Total QuickNode Credits Used in this session: ${credits}`);

//         // Create the new file name and path
//         const newFileName = `${token_address}.json`;
//         const newFilePath = path.join(directory, newFileName);

//         // Prepare the data to be saved
//         const dataToSave = {
//             tokenAAddress,
//             tokenBAddress
//         };

//         // Save the data to the new file
//         fs.writeFileSync(newFilePath, JSON.stringify(dataToSave, null, 2));

//         console.log(`Data saved to file: ${newFilePath}`);
//     } catch (error) {
//         console.error("Error fetching Raydium accounts:", error);
//     }
// }

// main(connection, raydium).catch(console.error);
const { Connection, PublicKey } = require("@solana/web3.js");
const fs = require('fs');
const path = require('path');

const SESSION_HASH = 'QNDEMO' + Math.ceil(Math.random() * 1e9); // Random unique identifier for your session
let credits = 0;

const SOLANA_ENDPOINT = 'https://fabled-misty-putty.solana-mainnet.quiknode.pro/d6c562f9b1106b60e01c276a42c58a1c182298c4/';
const raydium = new PublicKey('675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8');
const connection = new Connection(SOLANA_ENDPOINT, {
    wsEndpoint: SOLANA_ENDPOINT.replace('https://', 'wss://'),
    httpHeaders: { "x-session-hash": SESSION_HASH }
});

// Ensure the directory exists
const directory = './new_tokens';
if (!fs.existsSync(directory)) {
    fs.mkdirSync(directory, { recursive: true });
}

// Polling interval (1 second)
const POLLING_INTERVAL = 1000;

// Keep track of the last processed signature
let lastProcessedSignature = null;

// Monitor logs by polling every second and grabbing all unprocessed transactions
async function main(connection, programAddress) {
    console.log("Monitoring logs for program:", programAddress.toString());

    // Poll logs every second
    setInterval(async () => {
        try {
            // Fetch multiple signatures that haven't been processed yet
            const options = lastProcessedSignature ? { before: lastProcessedSignature, limit: 10 } : { limit: 10 };
            const logs = await connection.getConfirmedSignaturesForAddress2(programAddress, options);

            // If we have new signatures, process them
            if (logs && logs.length > 0) {
                for (const log of logs) {
                    const { signature } = log;

                    // Skip already processed signatures
                    if (signature === lastProcessedSignature) continue;

                    // console.log("New signature found:", signature);

                    // Process the transaction
                    await fetchRaydiumAccounts(signature, connection);

                    // Update last processed signature to the current one
                    lastProcessedSignature = signature;
                }
            }
        } catch (error) {
            console.error("Error fetching signatures:", error);
        }
    }, POLLING_INTERVAL);
}

// Fetch and process Raydium transaction data
async function fetchRaydiumAccounts(txId, connection) {
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

        // Check if tokenBAddress starts with "So1"
        if (!tokenBAddress.startsWith("So1")) {
            // console.log("No new coin detected.");
            return;  // Exit early if tokenBAddress does not start with "So1"
        }

        const token_address = tokenAAddress.startsWith("So1") ? tokenBAddress : tokenAAddress;

        console.log(`Transaction URL: https://solscan.io/tx/${txId}`);
        console.log(`Token A Account Public Key: ${tokenAAddress}`);
        console.log(`Token B Account Public Key: ${tokenBAddress}`);
        console.log(`Final Token Account Public Key: ${token_address}`);
        console.log(`Total QuickNode Credits Used in this session: ${credits}`);

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

        console.log(`Data saved to file: ${newFilePath}`);
    } catch (error) {
        console.error("Error fetching Raydium accounts:", error);
    }
}

// Start monitoring logs
main(connection, raydium).catch(console.error);
