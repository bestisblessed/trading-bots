const { Connection, PublicKey } = require("@solana/web3.js");
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process'); // Add this line
const transactionQueue = [];
let isProcessingQueue = false;

// const RAYDIUM_PUBLIC_KEY = process.env.RAYDIUM_PUBLIC_KEY;
// const SOLANA_ENDPOINT = process.env.SOLANA_ENDPOINT;
const SESSION_HASH = 'QNDEMO' + Math.ceil(Math.random() * 1e9); // Random unique identifier for your session
let credits = 0;

const SOLANA_ENDPOINT = 'https://api.mainnet-beta.solana.com/';
const raydium = new PublicKey('675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8');
const connection = new Connection(SOLANA_ENDPOINT, {
    wsEndpoint: SOLANA_ENDPOINT.replace('https://', 'wss://'),
    httpHeaders: {"x-session-hash": SESSION_HASH}
});

// Ensure the directory exists
const directory = './new_tokens';
if (!fs.existsSync(directory)) {
    fs.mkdirSync(directory, { recursive: true });
}

// Monitor logs
async function main(connection, programAddress) {
    console.log("Monitoring logs for program:", programAddress.toString());
    connection.onLogs(
        programAddress,
        ({ logs, err, signature }) => {
            if (err) return;

            if (logs && logs.some(log => log.includes("initialize2"))) {
                console.log("Signature for 'initialize2':", signature);
                fetchRaydiumAccounts(signature, connection);
            }
        },
        "finalized"
    );
}

// // Parse transaction and filter data
// async function fetchRaydiumAccounts(txId, connection) {
//     const tx = await connection.getParsedTransaction(
//         txId,
//         {
//             maxSupportedTransactionVersion: 0,
//             commitment: 'confirmed'
//         });

//     credits += 100;

//     // const accounts = tx?.transaction.message.instructions.find(ix => ix.programId.toBase58() === '675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8').accounts;
//     // if (!accounts) {
//     //     console.log("No accounts found in the transaction.");
//     //     return;
//     // }

//     // Extract the instruction
//     const instruction = tx?.transaction.message.instructions.find(ix => ix.programId.toBase58() === '675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8');

//     // Safely access accounts
//     const accounts = instruction?.accounts;

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

//     // Check if the token has already been processed
//     const newFileName = `${token_address}.json`;
//     const newFilePath = path.join(directory, newFileName);

//     if (fs.existsSync(newFilePath)) {
//         console.log(`Token ${token_address} has already been processed. Skipping.`);
//         return;
//     }

//     console.log(`Final Token Account Public Key: ${token_address}`);

//     // Prepare the data to be saved
//     const dataToSave = {
//         tokenAAddress,
//         tokenBAddress
//     };

//     // Save the data to the new file
//     fs.writeFileSync(newFilePath, JSON.stringify(dataToSave, null, 2));
//     console.log(`Data saved to file: ${newFilePath}`);

// //     // // Add the token address to the queue
// //     // transactionQueue.push(token_address);
// //     // processQueue();

// //     // Execute rug_detector_final.js with the token_address
// //     const command = `node rug_detector_final.js ${token_address}`;
// //     exec(command, (error, stdout, stderr) => {
// //         if (error) {
// //             console.error(`Error executing rug_detector_final.js: ${error}`);
// //             return;
// //         }
// //         if (stderr) {
// //             console.error(`Error output from rug_detector_final.js: ${stderr}`);
// //         }
// //         console.log(`rug_detector_final.js output:\n${stdout}`);
// //     });

// // }


//     // Add a 60-second (60000 ms) delay before running rug_detector
//     const delayInMilliseconds = 30000; // 60 seconds
//     setTimeout(() => {
//         // Execute rug_detector_final.js with the token_address after 60 seconds
//         const command = `node rug_detector_final.js ${token_address}`;
//         exec(command, (error, stdout, stderr) => {
//             if (error) {
//                 console.error(`Error executing rug_detector_final.js: ${error}`);
//                 return;
//             }
//             if (stderr) {
//                 console.error(`Error output from rug_detector_final.js: ${stderr}`);
//             }
//             console.log(`rug_detector_final.js output:\n${stdout}`);
//         });
//     }, delayInMilliseconds);
// }
// Function to wait for a specified time (ms)
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Enhanced fetchRaydiumAccounts with retry logic
async function fetchRaydiumAccounts(txId, connection, retries = 5) {
    let attempts = 0;
    const maxRetries = retries;
    let delay = 500; // Start with a 500ms delay for backoff

    while (attempts < maxRetries) {
        try {
            // Try fetching the transaction
            const tx = await connection.getParsedTransaction(
                txId,
                {
                    maxSupportedTransactionVersion: 0,
                    commitment: 'confirmed'
                });

            credits += 100;

            const instruction = tx?.transaction.message.instructions.find(ix => ix.programId.toBase58() === '675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8');
            const accounts = instruction?.accounts;

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

            const newFileName = `${token_address}.json`;
            const newFilePath = path.join(directory, newFileName);

            if (fs.existsSync(newFilePath)) {
                console.log(`Token ${token_address} has already been processed. Skipping.`);
                return;
            }

            console.log(`Final Token Account Public Key: ${token_address}`);

            const dataToSave = {
                tokenAAddress,
                tokenBAddress
            };

            fs.writeFileSync(newFilePath, JSON.stringify(dataToSave, null, 2));
            console.log(`Data saved to file: ${newFilePath}`);

            const delayInMilliseconds = 30000; // 30 seconds
            setTimeout(() => {
                const command = `node rug_detector_final.js ${token_address}`;
                exec(command, (error, stdout, stderr) => {
                    if (error) {
                        console.error(`Error executing rug_detector_final.js: ${error}`);
                        return;
                    }
                    if (stderr) {
                        console.error(`Error output from rug_detector_final.js: ${stderr}`);
                    }
                    console.log(`rug_detector_final.js output:\n${stdout}`);
                });
            }, delayInMilliseconds);

            break; // Break out of the retry loop on success

        } catch (error) {
            if (error.message.includes('429')) {
                // Handle rate-limiting (Too Many Requests)
                attempts++;
                console.log(`Server responded with 429 Too Many Requests. Retrying after ${delay}ms...`);
                await sleep(delay); // Wait before retrying
                delay *= 2; // Exponential backoff
            } else {
                // For any other errors, log them and exit the loop
                console.error(`Error fetching transaction: ${error}`);
                return;
            }
        }
    }

    if (attempts >= maxRetries) {
        console.error(`Max retries reached. Failed to fetch transaction for txId: ${txId}`);
    }
}

main(connection, raydium).catch(console.error);

    // // Delay execution by 2 minutes (120,000 milliseconds)
    // console.log('Waiting 20 seconds..')
    // const delayInMilliseconds = 20000;
    // setTimeout(() => {
    //     // Execute rug_detector_final.js with the token_address
    //     const command = `node ./rug_detector_final.js ${token_address}`;
    //     exec(command, (error, stdout, stderr) => {
    //         if (error) {
    //             console.error(`Error executing rug_detector_final.js: ${error}`);
    //             console.error(`Error output: ${stderr}`);
    //             return;
    //         }
    //         console.log(`rug_detector_final.js output:\n${stdout}`);
    //     });

    // }, delayInMilliseconds);

// }

// // # Process Queue
// function processQueue() {
//     if (isProcessingQueue) {
//         // Already processing the queue
//         return;
//     }
//     if (transactionQueue.length === 0) {
//         // Queue is empty
//         return;
//     }
//     isProcessingQueue = true;

//     const token_address = transactionQueue.shift();

//     // Delay execution by 20 seconds
//     const delayInMilliseconds = 40000; // 20 seconds
//     setTimeout(() => {
//         // Execute rug_detector_final.js with the token_address
//         const command = `node ./rug_detector_final.js ${token_address}`;
//         exec(command, (error, stdout, stderr) => {
//             if (error) {
//                 console.error(`Error executing rug_detector_final.js: ${error}`);
//                 console.error(`Error output: ${stderr}`);
//             } else {
//                 console.log(`rug_detector_final.js output:\n${stdout}`);
//             }
//             isProcessingQueue = false;
//             processQueue(); // Process next token in the queue
//         });
//     }, delayInMilliseconds);
// }


// main(connection, raydium).catch(console.error);



// EXECUTING DIRECTLY
//     // Save the data to the new file
//     fs.writeFileSync(newFilePath, JSON.stringify(dataToSave, null, 2));
//     console.log(`Data saved to file: ${newFilePath}`);

//     // Invoke rugDetector and processRankings directly
//     rugDetector(token_address).then(() => {
//         processRankings();
//     }).catch(error => {
//         console.error(`Error in rug detection: ${error}`);
//     });
// }
