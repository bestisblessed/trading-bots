const axios = require('axios');
const chalk = require('chalk');
const fs = require('fs');
const path = require('path');

// Suppress deprecation warnings
process.noDeprecation = true;

// List of token mint addresses to inspect
// const mintAddresses = [
//     'C1YhxP4gnnGnbGAe3VhxdQV4LGqmsXxFFb2HHL3tpump',
//     '4qkLHhLqrzeJCkC61XF82F4FieUzrqX6nzzEWG7rjPNC',
//     'Ft379JgZeZiUpdgeZ2at1vrua6BRZ4zSxAzJA97pump',
//     'UWp9ywERPuAFVQLNFt1tbfHCbaho8nuUKLzi8jupump',
//     '3M2vepByfZTG6xUSmFidvSCFzHWFoVw7cPvyRDnUpump',
//     '5xmnJLPMAgHSpLDR5GMuBWokw7yNdBCHBsV8ooAxpump',
//     'M49wideShuYwmnBMi3xXBoGnfg2TpTYAWyLt9QApump',
//     '2mnGSkXH1h6x5qmhwoQzAZDKa83vnRf8wNkNWVbdv7w5',
// ];
const walletAddress = '6ZDdVLFc2CRaPUwUGnfUsmXr32EBWoNaM9Axf5LWUjc6';
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

async function inspectLiquidity() {
    console.log(chalk.white.bold('\n\n\nInspecting Tokens & Pairs:\n'));
    console.log(chalk.grey('---------------------------------------------'));

    for (let mint of mintAddresses) {
        const dexData = await getDexscreenerData(mint);

        if (dexData && dexData.pairs && dexData.pairs.length > 0) {
            // console.log(chalk.green.italic(`Found pairs for Mint Address: ${mint}\n`));

            dexData.pairs.forEach(pair => {
                console.log(chalk.cyan(`Mint Address: ${mint}`));
                console.log(chalk.green(`  Name:`) + chalk.magenta(` ${pair.baseToken.name}`));
                console.log(chalk.green(`  Token:`) + chalk.magenta(` ${pair.baseToken.symbol}`));
                console.log(chalk.green(`  Pair:`) + chalk.magenta(` ${pair.baseToken.symbol}/${pair.quoteToken.symbol}`));
                console.log(chalk.green(`  DEX:`) + chalk.magenta(` ${pair.dexId}`));
                console.log(chalk.green(`  Liquidity:`) + chalk.magenta(` $${pair.liquidity.usd}`));
                console.log(chalk.green(`  Volume (24h):`) + chalk.magenta(` $${pair.volume.h24}`));
                console.log(chalk.green(`  Price:`) + chalk.magenta(` $${pair.priceUsd}`));
                
            });
        } else {
            console.log(chalk.red.italic(`No trading pairs found for Mint Address: ${mint}`));
        }
        console.log(chalk.grey('---------------------------------------------'));

        // Adding a delay between requests
        await sleep(2000); // 2-second delay
    }
}

// Execute the function
inspectLiquidity();
