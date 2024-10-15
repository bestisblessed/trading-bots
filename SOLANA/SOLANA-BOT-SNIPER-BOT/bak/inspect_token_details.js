const axios = require('axios');
const chalk = require('chalk');
const fs = require('fs');
const path = require('path');

// Suppress deprecation warnings
process.noDeprecation = true;

const walletAddress = process.argv[2]; // Get the wallet address from the command line arguments

const jsonFilePath = path.join(__dirname, 'data', `${walletAddress}_balance.json`);
const jsonData = JSON.parse(fs.readFileSync(jsonFilePath, 'utf8'));
const mintAddresses = jsonData.tokens.map(token => token.mint).filter(mint => mint !== 'So11111111111111111111111111111111111111112');

// Dexscreener API endpoint
const dexscreenerApiUrl = 'https://api.dexscreener.com/latest/dex/search?q=';

// Helper function to introduce a delay
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
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

async function inspectLiquidity() {
    console.log(chalk.white.bold('\n\nInspecting Tokens & Pairs in Wallet:\n'));
    console.log(chalk.grey('---------------------------------------------'));

    let outputData = {}; // Initialize an object to store output data

    for (let mint of mintAddresses) {
        const dexData = await getDexscreenerData(mint);

        if (dexData && dexData.pairs && dexData.pairs.length > 0) {
            console.log(chalk.cyan.bold(`\nFound pairs for Mint Address: ${mint}\n`));

            const tokenData = dexData.pairs.map(pair => {
                const liquidityUsd = pair.liquidity && pair.liquidity.usd ? pair.liquidity.usd : 'N/A';
                const volume24h = pair.volume && pair.volume.h24 ? pair.volume.h24 : 'N/A';
                const priceUsd = pair.priceUsd ? pair.priceUsd : 'N/A';

                console.log(chalk.green(`  Name:`) + chalk.magenta(` ${pair.baseToken.name}`));
                console.log(chalk.green(`  Token:`) + chalk.magenta(` ${pair.baseToken.symbol}`));
                console.log(chalk.green(`  Pair Address: ${pair.pairAddress}`));
                console.log(chalk.green(`  Pair:`) + chalk.magenta(` ${pair.baseToken.symbol}/${pair.quoteToken.symbol}`));
                console.log(chalk.green(`  DEX:`) + chalk.magenta(` ${pair.dexId}`));
                console.log(chalk.green(`  Liquidity:`) + chalk.magenta(` $${liquidityUsd}`));
                console.log(chalk.green(`  Volume (24h):`) + chalk.magenta(` $${volume24h}`));
                console.log(chalk.green(`  Price:`) + chalk.magenta(` $${priceUsd}`));
                console.log("");

                // Return pair data in a structured format
                return {
                    pairAddress: pair.pairAddress,
                    baseTokenName: pair.baseToken.name,
                    baseTokenSymbol: pair.baseToken.symbol,
                    quoteTokenSymbol: pair.quoteToken.symbol,
                    dexId: pair.dexId,
                    liquidityUsd: liquidityUsd,
                    volume24h: volume24h,
                    priceUsd: priceUsd,
                };
            });

            // Add the token data to the output object
            outputData[mint] = tokenData;

        } else {
            console.log(chalk.red.italic(`No trading pairs found for Mint Address: ${mint}`));
            outputData[mint] = "No trading pairs found";
        }

        console.log(chalk.grey('---------------------------------------------'));

        // Adding a delay between requests
        await sleep(500); // 1-second delay
    }

    // Get current timestamp
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-'); // Replace colon and dot characters to make it filename-safe

    // Define the output file path
    const outputFilePath = path.join(__dirname, 'data', `${walletAddress}_${timestamp}.json`);

    // Write the output data to the JSON file
    fs.writeFileSync(outputFilePath, JSON.stringify(outputData, null, 2), 'utf8');
    console.log(chalk.green(`\nOutput saved to: ${outputFilePath}`));
}

// Execute the function
inspectLiquidity();