const { Connection, PublicKey } = require("@solana/web3.js");
const fs = require('fs');
const path = require('path');

const SESSION_HASH = 'QNDEMO' + Math.ceil(Math.random() * 1e9); // Random unique identifier for your session
let credits = 0;

const SOLANA_ENDPOINT = 'https://tiniest-burned-mansion.solana-mainnet.quiknode.pro/a5f42fa1b144c8f334deb792e7567894965b96b0';

const raydium = new PublicKey('675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8');
const connection = new Connection(SOLANA_ENDPOINT, {
    wsEndpoint: SOLANA_ENDPOINT.replace('https://', 'wss://'),
    httpHeaders: {"x-session-hash": SESSION_HASH}
});

const directory = './new_tokens';
if (!fs.existsSync(directory)) {
    fs.mkdirSync(directory, { recursive: true });
}

// Variables for throttling
let lastFetchTime = 0;
const MIN_FETCH_INTERVAL = 3000; // Minimum time interval in milliseconds between fetches

// Monitor logs with optimized filtering
async function main(connection, programAddress) {
    console.log("Monitoring logs for program:", programAddress.toString());
    connection.onLogs(
        programAddress,
        async ({ logs, err, signature }) => {
            if (err) return;

            if (logs && logs.some(log => log.includes("initialize2"))) {
                const now = Date.now();
                
                // Throttle fetch calls to reduce excessive credit usage
                if (now - lastFetchTime >= MIN_FETCH_INTERVAL) {
                    lastFetchTime = now;
                    await fetchRaydiumAccounts(signature, connection);
                }
            }
        },
        "finalized"
    );
}

// Parse transaction and filter data with optimized usage
async function fetchRaydiumAccounts(txId, connection) {
    try {
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

        const token_address = tokenAAddress.startsWith("So1") ? tokenBAddress : tokenAAddress;

        console.log(`Transaction URL: https://solscan.io/tx/${txId}`);
        console.log(`Token A Account Public Key: ${tokenAAddress}`);
        console.log(`Token B Account Public Key: ${tokenBAddress}`);
        console.log(`Final Token Account Public Key: ${token_address}`);
        console.log(`Total QuickNode Credits Used in this session: ${credits}`);

        const newFileName = `${token_address}.json`;
        const newFilePath = path.join(directory, newFileName);

        const dataToSave = {
            tokenAAddress,
            tokenBAddress
        };

        fs.writeFileSync(newFilePath, JSON.stringify(dataToSave, null, 2));

        console.log(`Data saved to file: ${newFilePath}`);
    } catch (error) {
        console.error("Error fetching Raydium accounts:", error);
    }
}

main(connection, raydium).catch(console.error);

