const axios = require('axios');
const chalk = require('chalk');
const fs = require('fs');
const path = require('path');

// Suppress deprecation warnings
process.noDeprecation = true;

const walletAddress = process.argv[2]; // Get the wallet address from the command line arguments
const filePath = path.join(__dirname, 'data', `tokens_${walletAddress}.txt`);
const data = fs.readFileSync(filePath, 'utf8');
const mintAddresses = data.split('\n').filter(line => line.trim() !== '' && line.trim() !== 'So11111111111111111111111111111111111111112'); // Remove SOL address

// Solana RPC endpoint (you can use a public RPC URL or your own)
const solanaRpcUrl = 'https://api.mainnet-beta.solana.com';

// Dexscreener API endpoint
const dexscreenerApiUrl = 'https://api.dexscreener.com/latest/dex/search?q=';

// Helper function to introduce a delay
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Fetch the token balances for the wallet
async function getTokenBalances(walletAddress) {
    try {
        const response = await axios.post(solanaRpcUrl, {
            jsonrpc: "2.0",
            id: 1,
            method: "getTokenAccountsByOwner",
            params: [
                walletAddress,
                {
                    programId: "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
                },
                {
                    encoding: "jsonParsed"
                }
            ]
        });
        return response.data.result.value;
    } catch (error) {
        console.error(chalk.red('Error fetching token balances from Solana RPC:'), error);
        return null;
    }
}

async function inspectLiquidity() {
    console.log(chalk.white.bold('\n\n\nInspecting Tokens & Pairs:\n'));
    console.log(chalk.grey('---------------------------------------------'));

    const tokenBalances = await getTokenBalances(walletAddress);

    if (!tokenBalances) {
        console.log(chalk.red('Failed to retrieve token balances.'));
        return;
    }

    // Filter tokens to only include those with a balance greater than 0
    const tokensWithBalance = tokenBalances.filter(account => {
        const balance = parseFloat(account.account.data.parsed.info.tokenAmount.uiAmount);
        return balance > 0 && mintAddresses.includes(account.account.data.parsed.info.mint);
    });

    for (let account of tokensWithBalance) {
        const mint = account.account.data.parsed.info.mint;
        const balance = parseFloat(account.account.data.parsed.info.tokenAmount.uiAmount);

        const dexData = await getDexscreenerData(mint);

        if (dexData && dexData.pairs && dexData.pairs.length > 0) {
            console.log(chalk.yellow.bold(`Found pairs for Mint Address: ${mint} (Balance: ${balance})\n`));

            dexData.pairs.forEach(pair => {
                const liquidityUsd = pair.liquidity && pair.liquidity.usd ? pair.liquidity.usd : 'N/A';
                const volume24h = pair.volume && pair.volume.h24 ? pair.volume.h24 : 'N/A';
                const priceUsd = pair.priceUsd ? pair.priceUsd : 'N/A';

                console.log(chalk.cyan(`Pair Address: ${pair.pairAddress}`));
                console.log(chalk.green(`  Name:`) + chalk.magenta(` ${pair.baseToken.name}`));
                console.log(chalk.green(`  Token:`) + chalk.magenta(` ${pair.baseToken.symbol}`));
                console.log(chalk.green(`  Pair:`) + chalk.magenta(` ${pair.baseToken.symbol}/${pair.quoteToken.symbol}`));
                console.log(chalk.green(`  DEX:`) + chalk.magenta(` ${pair.dexId}`));
                console.log(chalk.green(`  Liquidity:`) + chalk.magenta(` $${liquidityUsd}`));
                console.log(chalk.green(`  Volume (24h):`) + chalk.magenta(` $${volume24h}`));
                console.log(chalk.green(`  Price:`) + chalk.magenta(` $${priceUsd}`));
                console.log(chalk.green(`  Current Balance:`) + chalk.magenta(` ${balance} ${pair.baseToken.symbol}`));
            });
        } else {
            console.log(chalk.red.italic(`No trading pairs found for Mint Address: ${mint}`));
        }
        console.log(chalk.grey('---------------------------------------------'));

        // Adding a delay between requests
        await sleep(1000); // 1-second delay
    }
}

// Execute the function
inspectLiquidity();
