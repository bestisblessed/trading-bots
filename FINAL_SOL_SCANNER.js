require('dotenv').config();
const { Connection, PublicKey } = require("@solana/web3.js");
const fs = require('fs');
const path = require('path');

const RAYDIUM_PUBLIC_KEY = process.env.RAYDIUM_PUBLIC_KEY;
const SOLANA_ENDPOINT = process.env.SOLANA_ENDPOINT;
const SESSION_HASH = 'QNDEMO' + Math.ceil(Math.random() * 1e9); // Random unique identifier for your session
let credits = 0;

const raydium = new PublicKey(RAYDIUM_PUBLIC_KEY);
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
    const tx = await connection.getParsedTransaction(
        txId,
        {
            maxSupportedTransactionVersion: 0,
            commitment: 'confirmed'
        });

    credits += 100;

    const accounts = tx?.transaction.message.instructions.find(ix => ix.programId.toBase58() === RAYDIUM_PUBLIC_KEY).accounts;

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
}

main(connection, raydium).catch(console.error);
