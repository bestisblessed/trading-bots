// const { rugDetector } = require('./rug_detector_final'); // assuming you have this in a separate file
// const { Connection, PublicKey } = require('@solana/web3.js');
// const fs = require('fs');
// const path = require('path');
// const transactionQueue = [];
// let isProcessingQueue = false;

// // Helper function to create a delay
// const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// const SESSION_HASH = 'QNDEMO' + Math.ceil(Math.random() * 1e9); // Random unique identifier for your session
// const SOLANA_ENDPOINT = 'https://api.mainnet-beta.solana.com/';
// const raydium = new PublicKey('675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8');
// const connection = new Connection(SOLANA_ENDPOINT, {
//     wsEndpoint: SOLANA_ENDPOINT.replace('https://', 'wss://'),
//     httpHeaders: { "x-session-hash": SESSION_HASH }
// });

// // Function to process each transaction
// async function processTransaction(txId, connection) {
//     try {
//         const tx = await connection.getParsedTransaction(
//             txId,
//             { maxSupportedTransactionVersion: 0, commitment: 'confirmed' }
//         );

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

//         // Call rugDetector function, which handles everything including liquidity checks
//         await rugDetector(token_address);

//     } catch (error) {
//         console.error(`Error processing transaction ${txId}:`, error);
//     }
// }

// main(connection, raydium).catch(console.error);
const { Connection, PublicKey } = require("@solana/web3.js");
const { getMint } = require('@solana/spl-token');
const fs = require('fs');
const path = require('path');
const processedTransactions = new Set();
const transactionQueue = [];
let isProcessingQueue = false;

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

// Ensure 'rug-detections' and 'rankings' directories exist
const rugDetectionsDir = path.join(__dirname, 'rug-detections');
const rankingsDir = path.join(__dirname, 'rankings');
if (!fs.existsSync(rugDetectionsDir)) {
    fs.mkdirSync(rugDetectionsDir, { recursive: true });
}
if (!fs.existsSync(rankingsDir)) {
    fs.mkdirSync(rankingsDir, { recursive: true });
}

// Function to detect rug and save token data
async function rugDetector(tokenMintAddress) {
    const connection = new Connection('https://api.mainnet-beta.solana.com', 'confirmed');
    const mintPublicKey = new PublicKey(tokenMintAddress);
    const mintInfo = await getMint(connection, mintPublicKey);

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
    };

    const filePath = path.join(rugDetectionsDir, `${tokenMintAddress}.json`);
    try {
        fs.writeFileSync(filePath, JSON.stringify(results, null, 2));
        console.log(`Data saved to ${filePath}`);
        applyRanking(results);
    } catch (error) {
        console.error(`Error saving file: ${error}`);
    }
}

// Ranking logic for the specific token
function applyRanking(tokenData) {
    const tokenMintAddress = tokenData.tokenMintAddress;
    let rank = 0;

    // Apply ranking rules
    if (tokenData.mintAuthority !== 'None' || tokenData.freezeAuthority !== 'None') {
        rank = 1;
    }

    if (tokenData.ownershipRenounced) {
        rank = 3;
    }

    if (tokenData.ownershipRenounced &&
        tokenData.mintAuthority === 'None' &&
        tokenData.freezeAuthority === 'None' &&
        tokenData.largestHolderPercentage < 50) {
        rank = 5;
    }

    if (rank === 0) {
        rank = 2;
    }

    const rankData = {
        tokenMintAddress: tokenMintAddress,
        rank: rank
    };

    const outputFilePath = path.join(rankingsDir, `${tokenMintAddress}.json`);
    try {
        fs.writeFileSync(outputFilePath, JSON.stringify(rankData, null, 2));
        console.log(`Processed ${tokenMintAddress} and assigned rank ${rank}`);
    } catch (error) {
        console.error(`Error saving rank file for ${tokenMintAddress}:`, error);
    }
}

// Main function to monitor the blockchain and scan for new tokens
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

// Enqueue the transaction for processing if not already processed
function fetchRaydiumAccounts(txId, connection) {
    if (!processedTransactions.has(txId)) {
        processedTransactions.add(txId);
        transactionQueue.push({ txId, connection });
        processQueue(); // Process the queue after adding a new transaction
    } else {
        console.log(`Transaction ${txId} has already been processed, skipping.`);
    }
}

// Process the queue sequentially
async function processQueue() {
    if (isProcessingQueue) return;
    isProcessingQueue = true;

    while (transactionQueue.length > 0) {
        const { txId, connection } = transactionQueue.shift();
        await processTransaction(txId, connection);
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

        // Introduce a 10-second delay before fetching token details
        console.log(`Waiting 10 seconds before fetching token details for ${token_address}...`);
        await delay(10000);

        // Fetch and print mint details and run rug detection
        await rugDetector(token_address);

    } catch (error) {
        console.error(`Error processing transaction ${txId}:`, error);
    }
}

main(connection, raydium).catch(console.error);
