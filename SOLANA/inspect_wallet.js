const solanaWeb3 = require('@solana/web3.js');
const chalk = require('chalk');
const fs = require('fs');
const path = require('path');

// Suppress deprecation warnings
process.noDeprecation = true;

// Solana wallet address
const walletAddress = '6ZDdVLFc2CRaPUwUGnfUsmXr32EBWoNaM9Axf5LWUjc6';
const walletPublicKey = new solanaWeb3.PublicKey(walletAddress);

// Connect to the Solana cluster (Mainnet, Devnet, or Testnet)
const connection = new solanaWeb3.Connection(solanaWeb3.clusterApiUrl('mainnet-beta'), 'confirmed');

// Helper function to introduce a delay
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function getWalletInfo() {
    try {
        // Fetch the wallet's balance
        console.log(chalk.cyan.bold('\nWallet Balance:'));
        const balance = await connection.getBalance(walletPublicKey);
        console.log(chalk.green.bold(`${balance / solanaWeb3.LAMPORTS_PER_SOL} SOL`));

        // Fetch the list of token accounts owned by the wallet
        console.log(chalk.cyan.bold('\nToken Accounts:'));
        const tokenAccounts = await connection.getParsedTokenAccountsByOwner(
            walletPublicKey,
            {
                programId: new solanaWeb3.PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
            }
        );

        // Create an array to store mint addresses
        let mintAddresses = [];
        
        tokenAccounts.value.forEach((accountInfo) => {
            const tokenAmount = accountInfo.account.data.parsed.info.tokenAmount.uiAmount;
            const mint = accountInfo.account.data.parsed.info.mint;
            console.log(chalk.magenta(`- Token Address: ${mint}, Amount: ${tokenAmount}`));
            mintAddresses.push(mint);
        });

        // Save mint addresses to a file in the 'data/' directory
        const filePath = path.join(__dirname, 'data', `tokens_${walletAddress}.txt`);
        fs.writeFileSync(filePath, mintAddresses.join('\n'), 'utf8');
        // console.log(chalk.black.italic(`Mint addresses saved to ${filePath}`));

        // Fetch the transaction history of the wallet
        console.log(chalk.cyan.bold('\nRecent Transactions:'));
        const confirmedSignatures = await connection.getConfirmedSignaturesForAddress2(
            walletPublicKey, 
            { limit: 10 }
        );

        for (let signature of confirmedSignatures) {
            console.log(chalk.green(`- Signature: ${signature.signature}`));
            let transaction = await connection.getConfirmedTransaction(signature.signature);
            console.log(chalk.greenBright(`  - Block Time: ${new Date(transaction.blockTime * 1000).toLocaleString()}`));
            console.log(chalk.greenBright(`  - Slot: ${transaction.slot}`));
            
            // Wait for 1 second before making the next request
            await sleep(2000);
        }

    } catch (error) {
        console.error(chalk.red('Error fetching wallet info:'), error);
    }
}

getWalletInfo();