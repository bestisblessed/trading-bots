// const { Connection, PublicKey } = require("@solana/web3.js");
// const { getMint } = require('@solana/spl-token');
// const fs = require('fs');
// const path = require('path');
// const { exec } = require('child_process');
// const axios = require('axios');
// const { rugDetector } = require('./rug_detector_final');

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

// // Queue for processing transactions
// const transactionQueue = [];
// let isProcessingQueue = false;

// // Monitor logs
// async function main(connection, programAddress) {
//     console.log("");
//     console.log("Monitoring Solana Blockchain...");
//     console.log("");
//     connection.onLogs(
//         programAddress,
//         ({ logs, err, signature }) => {
//             if (err) return;

//             if (logs && logs.some(log => log.includes("initialize2"))) {
//                 // Enqueue the transaction signature for processing
//                 fetchRaydiumAccounts(signature, connection);
//             }
//         },
//         "finalized"
//     );
// }

// // Enqueue the transaction for processing
// function fetchRaydiumAccounts(txId, connection) {
//     transactionQueue.push({ txId, connection });
//     processQueue();
// }

// // Process the queue sequentially
// async function processQueue() {
//     if (isProcessingQueue) return;
//     isProcessingQueue = true;

//     while (transactionQueue.length > 0) {
//         const { txId, connection } = transactionQueue.shift();
//         await processTransaction(txId, connection);
//         // Delay between processing each transaction
//         await delay(1500); // Adjust the delay as needed
//     }

//     isProcessingQueue = false;
// }

// // Process each transaction
// async function processTransaction(txId, connection) {
//     try {
//         const tx = await connection.getParsedTransaction(
//             txId,
//             {
//                 maxSupportedTransactionVersion: 0,
//                 commitment: 'confirmed'
//             });

//         credits += 100;

//         const accounts = tx?.transaction.message.instructions.find(ix => ix.programId.toBase58() === raydium.toBase58()).accounts;

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

//         // Fetch and print mint details
//         await fetchAndPrintMintDetails(token_address);

//     } catch (error) {
//         console.error(`Error processing transaction ${txId}:`, error);
//     }
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

//         // Print details to the console
//         console.log(`Mint Address: ${mintDetails.mintAddress}`);
//         console.log(`Total Supply: ${mintDetails.totalSupply}`);
//         console.log(`Decimals: ${mintDetails.decimals}`);
//         console.log(`Mint Authority: ${mintDetails.mintAuthority}`);
//         console.log(`Freeze Authority: ${mintDetails.freezeAuthority}`);
//         console.log(`Mint is Initialized: ${mintDetails.isInitialized}`);
//         console.log('------------------------');

//         // Call the RugCheck detection function using Python
//         runRugCheck(mintAddress);

//     } catch (error) {
//         console.error(`Error fetching details for mint ${mintAddress}:`, error);
//     }
// }

// // // Function to run the RugCheck detector
// // function runRugCheck(tokenMintAddress) {
// //     // Run the rug detection using the mint address
// //     exec(`python3 rugcheckxyz.py ${tokenMintAddress}`, (error, stdout, stderr) => {
// //         if (error) {
// //             console.error(`Error running rug detection: ${error.message}`);
// //             return;
// //         }
// //         if (stderr) {
// //             console.error(`Rug Detection Stderr: ${stderr}`);
// //             return;
// //         }
// //         console.log(`RugCheck Result: ${stdout}`);
// //     });
// // }

// // Function to run the rug detector
// async function runRugCheck(tokenMintAddress) {
//     await rugDetector(tokenMintAddress); // Call the JavaScript version instead of the Python script
// }

// main(connection, raydium).catch(console.error);
const { Connection, PublicKey } = require("@solana/web3.js");
const { getMint } = require('@solana/spl-token');
const fs = require('fs');
const path = require('path');
const axios = require('axios');

// Importing the delay function and child_process if needed
const { exec } = require('child_process');

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

// Ensure 'rug-detections' directory exists
const rugDetectionsDir = path.join(__dirname, 'rug-detections');
if (!fs.existsSync(rugDetectionsDir)) {
    fs.mkdirSync(rugDetectionsDir, { recursive: true });
}

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
        await delay(1500); // Adjust the delay as needed
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

        // Call the RugCheck detection function using Node.js
        await rugDetector(mintAddress);

    } catch (error) {
        console.error(`Error fetching details for mint ${mintAddress}:`, error);
    }
}

/**
 * Function to fetch liquidity from Dexscreener API
 */
async function getLiquidityInfo(tokenMintAddress) {
    const apiUrl = `https://api.dexscreener.com/latest/dex/tokens/${tokenMintAddress}`;

    try {
        const response = await axios.get(apiUrl);
        const data = response.data;

        if (data && data.pairs && data.pairs.length > 0) {
            // Get the first pair from the response
            const pair = data.pairs[0];
            const liquidityUsd = pair.liquidity ? pair.liquidity.usd : 0;
            return liquidityUsd;
        } else {
            console.log(`No liquidity information found for token ${tokenMintAddress}.`);
            return 0;
        }
    } catch (error) {
        console.error(`Error fetching liquidity info: ${error}`);
        return 0;
    }
}

/**
 * Rug Pull Detection Function
 */
// async function rugDetector(tokenMintAddress) {
//     const connection = new Connection('https://api.mainnet-beta.solana.com', 'confirmed');
//     const mintPublicKey = new PublicKey(tokenMintAddress);
//     const mintInfo = await getMint(connection, mintPublicKey);

//     if (mintInfo.freezeAuthority) {
//         console.log(`FAIL: Token ${tokenMintAddress} is freezeable. Freeze Authority: ${mintInfo.freezeAuthority.toBase58()}`);
//     } else {
//         console.log(`PASS: Token ${tokenMintAddress} is not freezeable.`);
//     }

//     if (mintInfo.mintAuthority) {
//         console.log(`FAIL: Token ${tokenMintAddress} has a mint authority: ${mintInfo.mintAuthority.toBase58()}`);
//     } else {
//         console.log(`PASS: Token ${tokenMintAddress} does not have a mint authority.`);
//     }

//     if (!mintInfo.mintAuthority && !mintInfo.freezeAuthority) {
//         console.log(`PASS: Token ${tokenMintAddress} has renounced ownership (no mint or freeze authority).`);
//     } else {
//         console.log(`FAIL: Token ${tokenMintAddress} has not renounced ownership.`);
//     }

//     const largestAccounts = await connection.getTokenLargestAccounts(mintPublicKey);

//     console.log(`Top holders for token ${tokenMintAddress}:`);
//     largestAccounts.value.forEach((accountInfo, index) => {
//         console.log(`  ${index + 1}. Account: ${accountInfo.address.toBase58()}, Amount: ${accountInfo.uiAmount}`);
//     });

//     const topHolderThreshold = 50;
//     const largestHolder = largestAccounts.value[0];
//     if (largestHolder && largestHolder.uiAmount > topHolderThreshold) {
//         console.log(`FAIL: Largest holder owns more than ${topHolderThreshold}% of the token supply.`);
//     } else {
//         console.log(`PASS: No holder owns more than ${topHolderThreshold}% of the token supply.`);
//     }

//     const liquidityUsd = await getLiquidityInfo(tokenMintAddress);
//     if (liquidityUsd < 10000) {
//         console.log(`FAIL: Token ${tokenMintAddress} has low liquidity ($${liquidityUsd}).`);
//     } else {
//         console.log(`PASS: Token ${tokenMintAddress} has sufficient liquidity $${liquidityUsd}.`);
//     }

//     const results = {
//         tokenMintAddress,
//         freezeAuthority: mintInfo.freezeAuthority ? mintInfo.freezeAuthority.toBase58() : 'None',
//         mintAuthority: mintInfo.mintAuthority ? mintInfo.mintAuthority.toBase58() : 'None',
//         ownershipRenounced: !mintInfo.mintAuthority && !mintInfo.freezeAuthority,
//         topHolders: largestAccounts.value.map((accountInfo, index) => ({
//             rank: index + 1,
//             account: accountInfo.address.toBase58(),
//             amount: accountInfo.uiAmount,
//         })),
//         largestHolderPercentage: largestHolder && largestHolder.uiAmount > topHolderThreshold ? largestHolder.uiAmount : 0,
//         liquidity: liquidityUsd
//     };

//     const filePath = path.join(rugDetectionsDir, `${tokenMintAddress}.json`);
//     try {
//         fs.writeFileSync(filePath, JSON.stringify(results, null, 2));
//         console.log(`Data saved to ${filePath}`);
//     } catch (error) {
//         console.error(`Error saving file: ${error}`);
//     }
// }
async function rugDetector(tokenMintAddress) {
    const mintPublicKey = new PublicKey(tokenMintAddress);
    const mintInfo = await getMint(connection, mintPublicKey);

    // Rug detection logic (unchanged from before)
    if (mintInfo.freezeAuthority) {
        console.log(`FAIL: Token ${tokenMintAddress} is freezeable. Freeze Authority: ${mintInfo.freezeAuthority.toBase58()}`);
    } else {
        console.log(`PASS: Token ${tokenMintAddress} is not freezeable.`);
    }

    if (mintInfo.mintAuthority) {
        console.log(`FAIL: Token ${tokenMintAddress} has a mint authority: ${mintInfo.mintAuthority.toBase58()}`);
    } else {
        console.log(`PASS: Token ${tokenMintAddress} does not have a mint authority.`);
    }

    if (!mintInfo.mintAuthority && !mintInfo.freezeAuthority) {
        console.log(`PASS: Token ${tokenMintAddress} has renounced ownership (no mint or freeze authority).`);
    } else {
        console.log(`FAIL: Token ${tokenMintAddress} has not renounced ownership.`);
    }

    const largestAccounts = await connection.getTokenLargestAccounts(mintPublicKey);
    console.log(`Top holders for token ${tokenMintAddress}:`);
    largestAccounts.value.forEach((accountInfo, index) => {
        console.log(`  ${index + 1}. Account: ${accountInfo.address.toBase58()}, Amount: ${accountInfo.uiAmount}`);
    });

    const topHolderThreshold = 50;
    const largestHolder = largestAccounts.value[0];
    if (largestHolder && largestHolder.uiAmount > topHolderThreshold) {
        console.log(`FAIL: Largest holder owns more than ${topHolderThreshold}% of the token supply.`);
    } else {
        console.log(`PASS: No holder owns more than ${topHolderThreshold}% of the token supply.`);
    }

    const liquidityUsd = await getLiquidityInfo(tokenMintAddress);
    if (liquidityUsd < 10000) {
        console.log(`FAIL: Token ${tokenMintAddress} has low liquidity ($${liquidityUsd}).`);
    } else {
        console.log(`PASS: Token ${tokenMintAddress} has sufficient liquidity $${liquidityUsd}.`);
    }

    const results = {
        tokenMintAddress,
        freezeAuthority: mintInfo.freezeAuthority ? mintInfo.freezeAuthority.toBase58() : 'None',
        mintAuthority: mintInfo.mintAuthority ? mintInfo.mintAuthority.toBase58() : 'None',
        ownershipRenounced: !mintInfo.mintAuthority && !mintInfo.freezeAuthority,
        topHolders: largestAccounts.value.map((accountInfo, index) => ({
            rank: index + 1,
            account: accountInfo.address.toBase58(),
            amount: accountInfo.uiAmount,
        })),
        largestHolderPercentage: largestHolder && largestHolder.uiAmount > topHolderThreshold ? largestHolder.uiAmount : 0,
        liquidity: liquidityUsd
    };

    // Save the rug detection results to 'rug-detections/' folder
    const filePath = path.join(rugDetectionsDir, `${tokenMintAddress}.json`);
    try {
        fs.writeFileSync(filePath, JSON.stringify(results, null, 2));
        console.log(`Data saved to ${filePath}`);
    } catch (error) {
        console.error(`Error saving file: ${error}`);
    }

    // Ranking logic
    if (!fs.existsSync('./rankings/')) {
        fs.mkdirSync('./rankings/');
    }

    // Read the saved JSON and apply the ranking logic
    fs.readdir('./rug-detections/', (err, files) => {
        if (err) {
            return console.error('Error reading directory:', err);
        }

        files.forEach(file => {
            if (file.endsWith(`${tokenMintAddress}.json`)) { // Only process the current token
                const filePath = path.join('./rug-detections/', file);
                const tokenData = JSON.parse(fs.readFileSync(filePath, 'utf8'));

                let rank = 0;

                // Apply ranking rules
                if (tokenData.liquidity < 999) {
                    rank = 1;
                }

                if (tokenData.mintAuthority !== 'None' || tokenData.freezeAuthority !== 'None') {
                    rank = 1;
                }

                if (tokenData.liquidity > 10000 && tokenData.ownershipRenounced) {
                    rank = 3;
                }

                if (tokenData.liquidity > 10000 &&
                    tokenData.ownershipRenounced &&
                    tokenData.mintAuthority === 'None' &&
                    tokenData.freezeAuthority === 'None') {
                    rank = 4;
                }

                if (tokenData.liquidity > 10000 &&
                    tokenData.ownershipRenounced &&
                    tokenData.mintAuthority === 'None' &&
                    tokenData.freezeAuthority === 'None' &&
                    tokenData.largestHolderPercentage < 50) {
                    rank = 5;
                }

                // Assign a default score if no rules matched
                if (rank === 0) {
                    rank = 2;
                }

                const rankData = {
                    tokenMintAddress: tokenData.tokenMintAddress,
                    rank: rank
                };

                const outputFilePath = path.join('./rankings/', `${tokenData.tokenMintAddress}_rank.json`);
                try {
                    fs.writeFileSync(outputFilePath, JSON.stringify(rankData, null, 2));
                    console.log(`Processed ${tokenData.tokenMintAddress} and assigned rank ${rank}`);
                    console.log('------------------------');
                } catch (error) {
                    console.error(`Error saving rank file for ${tokenData.tokenMintAddress}:`, error);
                    console.log('------------------------');
                }
            }
        });
    });
}


// function runRugCheck(tokenMintAddress) {
//     // Run the rug detection using the mint address
//     exec(`python3 assign_token_rankins.py ${tokenMintAddress}`, (error, stdout, stderr) => {
//         if (error) {
//             console.error(`Error running rug detection: ${error.message}`);
//             return;
//         }
//         if (stderr) {
//             console.error(`Rug Detection Stderr: ${stderr}`);
//             return;
//         }
//         console.log(`RugCheck Result: ${stdout}`);
//     });
// }

main(connection, raydium).catch(console.error);


