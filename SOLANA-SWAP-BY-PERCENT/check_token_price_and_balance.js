const solanaWeb3 = require('@solana/web3.js');
const axios = require('axios');
const chalk = require('chalk');
const fs = require('fs');
const path = require('path');

// Suppress deprecation warnings
process.noDeprecation = true;

// Get the mint address from the command line arguments
const input = process.argv[2];

// Check if the mint address is provided
if (!input) {
    console.error(chalk.red.bold('Error: A coin address (mint address) must be provided as an argument.'));
    process.exit(1); // Exit the script with an error code
}

// Hardcoded Solana wallet address
const hardcodedWalletAddress = 'C9WLhFLSX1LomVf3DGV4RyVqxqDSNg7BFr8YaTEzCajs';
const walletPublicKey = new solanaWeb3.PublicKey(hardcodedWalletAddress);
const connection = new solanaWeb3.Connection(solanaWeb3.clusterApiUrl('mainnet-beta'), 'confirmed');

// Ensure 'data/' directory exists
const dataDir = path.join(__dirname, 'data');
if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir);
}

// Define the output file path for the mint addresses
const txtFilePath = path.join(dataDir, `tokens_${hardcodedWalletAddress}.txt`);

// Dexscreener API endpoint
const dexscreenerApiUrl = 'https://api.dexscreener.com/latest/dex/search?q=';

// Command-line arguments
let mintAddresses = [];
let totalSolBalance = 0; // Initialize total SOL balance

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
            mintAddresses.push({ mint, amount: tokenAmount }); // Store mint addresses and amounts for Dexscreener inspection
        });

        console.log(chalk.black.italic(`\nMint addresses saved to ${txtFilePath}`));

    } catch (error) {
        console.error(chalk.red('Error fetching wallet info:'), error);
    }
}

async function getDexscreenerData(mintAddress) {
    try {
        const response = await axios.get(`${dexscreenerApiUrl}${mintAddress}`);
        return response.data;
    } catch (error) {
        console.error(chalk.red('Error fetching data from Dexscreener API:'), error);
        return null;
    }
}

async function inspectToken(mintAddress, tokenAmount = null) {
    console.log(chalk.cyan.bold('\nInspecting Token:\n'));

    // If tokenAmount is null, try to find it in mintAddresses
    if (tokenAmount === null) {
        const tokenData = mintAddresses.find(token => token.mint === mintAddress);
        if (tokenData) {
            tokenAmount = tokenData.amount;
        }
    }

    const dexData = await getDexscreenerData(mintAddress);

    if (dexData && dexData.pairs && dexData.pairs.length > 0) {
        console.log(chalk.yellow.italic(`Found pairs for Mint Address: ${mintAddress}\n`));

        dexData.pairs.forEach(pair => {
            // Extract pair data safely with checks for undefined fields
            const liquidityUsd = pair.liquidity && pair.liquidity.usd ? pair.liquidity.usd : 'N/A';
            const volume24h = pair.volume && pair.volume.h24 ? pair.volume.h24 : 'N/A';
            const priceUsd = pair.priceUsd ? pair.priceUsd : 'N/A';
            const priceSol = pair.priceNative ? parseFloat(pair.priceNative) : 0; // Get price in SOL if available

            console.log(chalk.cyan(`Pair Address: ${pair.pairAddress}`));
            console.log(chalk.green(`  Name:`) + chalk.magenta(` ${pair.baseToken.name}`));
            console.log(chalk.green(`  Token:`) + chalk.magenta(` ${pair.baseToken.symbol}`));
            console.log(chalk.green(`  Pair:`) + chalk.magenta(` ${pair.baseToken.symbol}/${pair.quoteToken.symbol}`));
            console.log(chalk.green(`  DEX:`) + chalk.magenta(` ${pair.dexId}`));
            console.log(chalk.green(`  Liquidity:`) + chalk.magenta(` $${liquidityUsd}`));
            console.log(chalk.green(`  Volume (24h):`) + chalk.magenta(` $${volume24h}`));
            console.log(chalk.green(`  Price (USD):`) + chalk.magenta(` $${priceUsd}`));
            console.log(chalk.green(`  Price (SOL):`) + chalk.magenta(` ${priceSol} SOL`));

            // Debugging: Log token amount and price to ensure correct values
            console.log(chalk.red.bold(`  DEBUG: Token Amount: ${tokenAmount}`));
            console.log(chalk.red.bold(`  DEBUG: Price (SOL): ${priceSol}`));

            // Calculate and accumulate SOL value for the token
            if (priceSol > 0 && tokenAmount > 0) {
                const solEquivalent = tokenAmount * priceSol; // Multiply token amount by SOL price
                totalSolBalance += solEquivalent; // Accumulate to total SOL balance
                // console.log(chalk.blue.bold(`You have approximately ${solEquivalent.toFixed(6)} SOL worth of ${pair.baseToken.symbol}`));
            }
        });
    } else {
        console.log(chalk.red.italic(`No trading pairs found for Mint Address: ${mintAddress}`));
    }
    console.log(chalk.grey('\n---------------------------------------------'));
}

// Function to print and save the total SOL balance
function printTotalSolBalance() {
    console.log(chalk.green.bold(`\nTotal SOL Balance from Tokens: ${totalSolBalance.toFixed(6)} SOL`));

    // Define the output file path for the SOL balance
    const solBalanceFilePath = path.join(dataDir, `total_sol_balance.txt`);

    // Write the total SOL balance to a file
    fs.writeFileSync(solBalanceFilePath, `Total SOL Balance: ${totalSolBalance.toFixed(6)} SOL`, 'utf8');
    
    console.log(chalk.grey.italic(`\nTotal SOL Balance saved to ${solBalanceFilePath}`));
}

async function inspectLiquidity() {
    console.log(chalk.white.bold('\n\n\nInspecting Tokens & Pairs:\n'));
    console.log(chalk.grey('---------------------------------------------'));

    for (let { mint, amount } of mintAddresses) {
        await inspectToken(mint, amount); // Pass the token amount to the inspectToken function
        await sleep(2000); // 2-second delay
    }

    // Print the total SOL balance at the end
    printTotalSolBalance();
}

// Main execution logic
(async function() {
    // First, inspect the hardcoded wallet
    await getWalletInfo();

    // Then, check the input mint address if provided and it's not the hardcoded wallet address
    if (input && input !== hardcodedWalletAddress) {
        await inspectToken(input);
        printTotalSolBalance(); // Print total SOL balance if inspecting a single token
    } else {
        // If no input is provided or the input matches the hardcoded wallet, inspect all tokens found in the wallet
        await inspectLiquidity();
    }

})();
