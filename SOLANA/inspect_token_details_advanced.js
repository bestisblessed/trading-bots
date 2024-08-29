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

// async function inspectLiquidity() {
//     console.log(chalk.white.bold('\n\n\nInspecting Tokens & Pairs:\n'));
//     console.log(chalk.grey('---------------------------------------------'));

//     for (let mint of mintAddresses) {
//         const dexData = await getDexscreenerData(mint);

//         if (dexData && dexData.pairs && dexData.pairs.length > 0) {
//             console.log(chalk.yellow.bold(`Found pairs for Mint Address: ${mint}\n`));
//             // console.log(chalk.cyan(`Mint Address: ${mint}`));

//             dexData.pairs.forEach(pair => {
//                 const liquidityUsd = pair.liquidity && pair.liquidity.usd ? pair.liquidity.usd : 'N/A';
//                 const volume24h = pair.volume && pair.volume.h24 ? pair.volume.h24 : 'N/A';
//                 const priceUsd = pair.priceUsd ? pair.priceUsd : 'N/A';
                
//                 // console.log(chalk.cyan(`Mint Address: ${mint}`));
//                 console.log(chalk.cyan(`Pair Address: ${pair.pairAddress}`));
//                 console.log(chalk.green(`  Name:`) + chalk.magenta(` ${pair.baseToken.name}`));
//                 console.log(chalk.green(`  Token:`) + chalk.magenta(` ${pair.baseToken.symbol}`));
//                 console.log(chalk.green(`  Pair:`) + chalk.magenta(` ${pair.baseToken.symbol}/${pair.quoteToken.symbol}`));
//                 console.log(chalk.green(`  DEX:`) + chalk.magenta(` ${pair.dexId}`));
//                 console.log(chalk.green(`  Liquidity:`) + chalk.magenta(` $${pair.liquidity.usd}`));
//                 console.log(chalk.green(`  Volume (24h):`) + chalk.magenta(` $${pair.volume.h24}`));
//                 console.log(chalk.green(`  Price:`) + chalk.magenta(` $${pair.priceUsd}`));
                
//             });
//         } else {
//             console.log(chalk.red.italic(`No trading pairs found for Mint Address: ${mint}`));
//         }
//         console.log(chalk.grey('---------------------------------------------'));

//         // Adding a delay between requests
//         await sleep(2000); // 2-second delay
//     }
// }
async function inspectLiquidity() {
    console.log(chalk.white.bold('\n\n\nInspecting Tokens & Pairs:\n'));
    console.log(chalk.grey('---------------------------------------------'));

    for (let mint of mintAddresses) {
        const dexData = await getDexscreenerData(mint);

        if (dexData && dexData.pairs && dexData.pairs.length > 0) {
            console.log(chalk.yellow.bold(`Found pairs for Mint Address: ${mint}\n`));

            dexData.pairs.forEach(pair => {
                // Extract pair data safely with checks for undefined fields
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
            });
        } else {
            console.log(chalk.red.italic(`No trading pairs found for Mint Address: ${mint}`));
        }
        console.log(chalk.grey('---------------------------------------------'));

        // Adding a delay between requests
        await sleep(1000); // 2-second delay
    }
}

// Execute the function
inspectLiquidity();