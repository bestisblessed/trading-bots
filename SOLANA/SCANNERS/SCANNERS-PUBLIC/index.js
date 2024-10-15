const { Connection, PublicKey } = require("@solana/web3.js");
const fs = require('fs');
const path = require('path');

// Use a public Solana RPC endpoint (Mainnet)
const SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com";
const connection = new Connection(SOLANA_RPC_URL, "confirmed");

// Unique session identifier
const SESSION_HASH = 'QNDEMO' + Math.ceil(Math.random() * 1e9);
let credits = 0;

const raydium = new PublicKey('675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8');

// Ensure the directory exists for saving tokens
const directory = './new_tokens';
if (!fs.existsSync(directory)) {
    fs.mkdirSync(directory, { recursive: true });
}

// Polling interval (1 second)
const POLLING_INTERVAL = 1000;

// Keep track of the last processed signature
let lastProcessedSignature = null;

// Monitor logs by polling every second and grabbing unprocessed transactions
async function main(connection, programAddress) {
    console.log("Monitoring transactions for program:", programAddress.toString());

    setInterval(async () => {
        try {
            // Fetch multiple signatures that haven't been processed yet
            const options = lastProcessedSignature ? { before: lastProcessedSignature, limit: 10 } : { limit: 10 };
            const logs = await connection.getConfirmedSignaturesForAddress2(programAddress, options);

            // If we have new signatures, process them
            if (logs && logs.length > 0) {
                for (const log of logs) {
                    const { signature } = log;

                    // Skip if this is the last processed signature
                    if (signature === lastProcessedSignature) continue;

                    console.log("New transaction detected:", signature);

                    // Process the transaction
                    await fetchRaydiumAccounts(signature, connection);

                    // Update last processed signature
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
            console.log("No new coin detected.");
            return;  // Exit early if tokenBAddress does not start with "So1"
        }

        const token_address = tokenAAddress.startsWith("So1") ? tokenBAddress : tokenAAddress;

        console.log(`Transaction URL: https://solscan.io/tx/${txId}`);
        console.log(`Token A Account Public Key: ${tokenAAddress}`);
        console.log(`Token B Account Public Key: ${tokenBAddress}`);
        console.log(`Final Token Account Public Key: ${token_address}`);
        console.log(`Total RPC Credits Used in this session: ${credits}`);

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
