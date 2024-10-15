const solanaWeb3 = require('@solana/web3.js');
const chalk = require('chalk');
const fs = require('fs');
const path = require('path');

// Suppress deprecation warnings
process.noDeprecation = true;

// Solana wallet address
const walletAddress = process.argv[2]; // Get the wallet address from the command line arguments
const walletPublicKey = new solanaWeb3.PublicKey(walletAddress);
const connection = new solanaWeb3.Connection(solanaWeb3.clusterApiUrl('mainnet-beta'), 'confirmed');

// Ensure 'data/' directory exists
const dataDir = path.join(__dirname, 'data');
if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir);
}

// Define the output file path for the mint addresses
const txtFilePath = path.join(dataDir, `tokens_${walletAddress}.txt`);

// Helper function to introduce a delay
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Helper function to log to console and save to file
function logAndSave(text, filePath) {
    console.log(text);
    fs.appendFileSync(filePath, text + '\n', 'utf8');
}

async function getWalletInfo() {
    try {
        // Start with a clean text output file
        fs.writeFileSync(txtFilePath, '', 'utf8');

        // Fetch the wallet's balance
        const balance = await connection.getBalance(walletPublicKey);
        console.log(chalk.cyan.bold('\nWallet Balance:'));
        console.log(chalk.green.bold(`${balance / solanaWeb3.LAMPORTS_PER_SOL} SOL`));

        // Fetch the list of token accounts owned by the wallet
        console.log(chalk.cyan.bold('\nToken Accounts:'));
        const tokenAccounts = await connection.getParsedTokenAccountsByOwner(
            walletPublicKey,
            {
                programId: new solanaWeb3.PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
            }
        );

        tokenAccounts.value.forEach((accountInfo) => {
            const tokenAmount = accountInfo.account.data.parsed.info.tokenAmount.uiAmount;
            const mint = accountInfo.account.data.parsed.info.mint;
            console.log(chalk.magenta(`- Token Address: ${mint}, Amount: ${tokenAmount}`));
            
            // Save each mint address to the text file, one per line
            fs.appendFileSync(txtFilePath, `${mint}\n`, 'utf8');
        });

        console.log(chalk.black.italic(`\nMint addresses saved to ${txtFilePath}`));

        // Fetch the transaction history of the wallet
        console.log(chalk.cyan.bold('\nRecent Transactions:'));
        const confirmedSignatures = await connection.getConfirmedSignaturesForAddress2(
            walletPublicKey, 
            { limit: 5 }
        );

        for (let signature of confirmedSignatures) {
            try {
                console.log(chalk.green(`- Signature: ${signature.signature}`));
                let transaction = await connection.getConfirmedTransaction(signature.signature);

                if (transaction) {
                    const blockTime = new Date(transaction.blockTime * 1000).toLocaleString();
                    console.log(chalk.greenBright(`  - Block Time: ${blockTime}`));
                    console.log(chalk.greenBright(`  - Slot: ${transaction.slot}`));
                } else {
                    console.log(chalk.yellow(`  - Transaction details not available for signature: ${signature.signature}`));
                }
            } catch (error) {
                if (error.code === -32015) {
                    console.log(chalk.yellow(`  - Skipping transaction with unsupported version (Signature: ${signature.signature})`));
                } else {
                    console.log(chalk.red('Error fetching transaction:'), error);
                }
            }
            
            await sleep(2000);
        }

    } catch (error) {
        console.error(chalk.red('Error fetching wallet info:'), error);
    }
}

getWalletInfo();
