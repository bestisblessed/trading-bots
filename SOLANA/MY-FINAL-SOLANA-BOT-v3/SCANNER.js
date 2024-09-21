const { Connection, PublicKey } = require("@solana/web3.js");
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process'); // Add this to import child_process

const SESSION_HASH = 'QNDEMO' + Math.ceil(Math.random() * 1e9); // Random unique identifier for your session

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

// Parse transaction and filter data
async function fetchRaydiumAccounts(txId, connection) {
    let tx;
    let attempts = 0;
    const maxAttempts = 10;
    const delay = 3000; // 3 seconds

    while (attempts < maxAttempts) {
        try {
            tx = await connection.getParsedTransaction(
                txId,
                {
                    maxSupportedTransactionVersion: 0,
                    commitment: 'confirmed'
                });
            break; // Break out of loop if the request is successful
        } catch (error) {
            if (error.message.includes("429 Too Many Requests")) {
                attempts++;
                console.log(`Server responded with 429 Too Many Requests. Retrying attempt ${attempts}/${maxAttempts} after ${delay / 1000}s delay...`);
                await new Promise(resolve => setTimeout(resolve, delay)); // Wait before retrying
            } else {
                console.error("Error fetching transaction:", error);
                return; // Exit if it's a different error
            }
        }
    }

    if (!tx) {
        console.log("Failed to fetch transaction after maximum retries. Moving on.");
        return; // Exit if unable to get the transaction after retries
    }

    const accounts = tx.transaction.message.instructions.find(ix => ix.programId.toBase58() === '675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8').accounts;

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

    console.log(`Transaction URL: https://solscan.io/tx/${txId}`);
    console.log(`Token A Account Public Key: ${tokenAAddress}`);
    console.log(`Token B Account Public Key: ${tokenBAddress}`);
    console.log(`Final Token Account Public Key: ${token_address}`);

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

    // // Execute the Python script after saving the data
    // exec('python 1_rug_detector_final.py', (error, stdout, stderr) => {
    //     if (error) {
    //         console.error(`Error executing Python script: ${error.message}`);
    //         return;
    //     }

    //     if (stderr) {
    //         console.error(stderr);
    //         return;
    //     }
        
    //     console.log(stdout);
    //     console.log('1_rug_detector_final.py executed successfully.');

    //     // After the Python script finishes, execute the 2_rug_detector_final.js script
    //     exec('node 2_rug_detector_final.js', (error, stdout, stderr) => {
    //         if (error) {
    //             console.error(`Error executing JavaScript script: ${error.message}`);
    //             return;
    //         }

    //         if (stderr) {
    //             console.error(stderr);
    //             return;
    //         }

    //         console.log(stdout);
    //         console.log('2_rug_detector_final.js executed successfully.');

    // Execute the Python script with the mint address
    exec(`python 1_rug_detector_final.py ${token_address}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error.message}`);
            return;
        }

        if (stderr) {
            console.error(stderr);
            return;
        }
        
        console.log(stdout);
        console.log('1_rug_detector_final.py executed successfully.');

        // After the Python script finishes, execute the 2_rug_detector_final.js script with the same mint address
        exec(`node 2_rug_detector_final.js ${token_address}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error executing 2_rug_detector_final.js: ${error.message}`);
                return;
            }

            if (stderr) {
                console.error(stderr);
                return;
            }

            console.log(stdout);
            console.log('2_rug_detector_final.js executed successfully.');
        });
    });
}

// Adding another script
//         // After 2_rug_detector_final.js finishes, execute the 3_rug_detector_final.js script
//         exec('node 3_rug_detector_final.js', (error, stdout, stderr) => {
//             if (error) {
//                 console.error(`Error executing 3_rug_detector_final.js: ${error.message}`);
//                 return;
//             }

//             if (stderr) {
//                 console.error(stderr);
//                 return;
//             }

//             console.log(stdout);
//             console.log('3_rug_detector_final.js executed successfully.');
//         });
//     });
// });


main(connection, raydium).catch(console.error);
