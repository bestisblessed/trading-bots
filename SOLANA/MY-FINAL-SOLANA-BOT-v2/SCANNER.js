const { Connection, PublicKey } = require("@solana/web3.js");
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process'); // Import child_process to run external scripts

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

// // Function to run `rug_detector_final.js` and return a promise to ensure sequential execution
// function runRugDetector(mintAddress) {
//     return new Promise((resolve, reject) => {
//         exec(`node rug_detector_final.js ${mintAddress}`, (error, stdout, stderr) => {
//             if (error) {
//                 console.error(`Error executing rug_detector_final.js: ${error.message}`);
//                 reject(error);
//             } else {
//                 if (stderr) {
//                     console.error(`stderr: ${stderr}`);
//                 }
//                 console.log(`stdout: ${stdout}`);
//                 resolve();
//             }
//         });
//     });
// }
// Function to run `rug_detector_final.js` and return a promise to ensure sequential execution
function runRugDetector(mintAddress) {
    console.log(`Running rug_detector_final.js with mint address: ${mintAddress}`); // Print the mint address
    return new Promise((resolve, reject) => {
        exec(`node rug_detector_final.js ${mintAddress}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error executing rug_detector_final.js: ${error.message}`);
                reject(error);
            } else {
                if (stderr) {
                    console.error(`stderr: ${stderr}`);
                }
                console.log(`stdout: ${stdout}`);
                resolve();
            }
        });
    });
}

const processedTokens = new Set();

async function fetchRaydiumAccounts(txId, connection) {
    try {
        const tx = await connection.getParsedTransaction(txId, { maxSupportedTransactionVersion: 0, commitment: 'confirmed' });
        credits += 100;

        const accounts = tx?.transaction.message.instructions.find(ix => ix.programId.toBase58() === '675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8').accounts;

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

        if (processedTokens.has(token_address)) {
            console.log(`Token ${token_address} already processed. Skipping.`);
            return;
        }

        processedTokens.add(token_address);

        const newFileName = `${token_address}.json`;
        const newFilePath = path.join(directory, newFileName);

        const dataToSave = {
            tokenAAddress,
            tokenBAddress
        };

        // Save the data to the new file
        fs.writeFileSync(newFilePath, JSON.stringify(dataToSave, null, 2));
        console.log(`Data saved to file: ${newFilePath}`);

        // After saving, run rug_detector_final.js with the mint address synchronously
        await runRugDetector(token_address);  // Ensure `rug_detector_final.js` completes before continuing

    } catch (error) {
        console.error(`Error processing transaction ${txId}:`, error);
    }
}

// Monitor logs
async function main(connection, programAddress) {
    console.log("Monitoring logs for program:", programAddress.toString());
    connection.onLogs(
        programAddress,
        async ({ logs, err, signature }) => {
            if (err) return;

            if (logs && logs.some(log => log.includes("initialize2"))) {
                await fetchRaydiumAccounts(signature, connection);
            }
        },
        "finalized"
    );
}

main(connection, raydium).catch(console.error);
