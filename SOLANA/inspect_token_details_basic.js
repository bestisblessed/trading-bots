// const fs = require('fs');
// const path = require('path');
// const chalk = require('chalk');
// const solanaWeb3 = require('@solana/web3.js');
// const splToken = require('@solana/spl-token');
// const { Metaplex, keypairIdentity, bundlrStorage, mockStorage } = require('@metaplex-foundation/js');

// // Suppress deprecation warnings
// process.noDeprecation = true;

// const walletAddress = '6ZDdVLFc2CRaPUwUGnfUsmXr32EBWoNaM9Axf5LWUjc6';
// const filePath = path.join(__dirname, 'data', `tokens_${walletAddress}.txt`);
// const data = fs.readFileSync(filePath, 'utf8');
// const mintAddresses = fs.readFileSync(filePath, 'utf8')
//     .split('\n')
//     .filter(line => line.trim() !== '' && line.trim() !== 'So11111111111111111111111111111111111111112'); // Remove SOL address
// // console.log(chalk.green('Mint Addresses:'), mintAddresses);

// // Connect to the Solana cluster (Mainnet, Devnet, or Testnet)
// const connection = new solanaWeb3.Connection(solanaWeb3.clusterApiUrl('mainnet-beta'), 'confirmed');

// // Initialize Metaplex
// const metaplex = new Metaplex(connection).use(mockStorage()); // Use mockStorage for simplicity

// // Helper function to introduce a delay
// function sleep(ms) {
//     return new Promise(resolve => setTimeout(resolve, ms));
// }

// // Function to fetch token information based on the mint address
// async function getTokenInfo(mintAddress) {
//     const mintPublicKey = new solanaWeb3.PublicKey(mintAddress);
//     const tokenInfo = await splToken.getMint(connection, mintPublicKey);

//     // Fetch metadata using the Metaplex SDK
//     const nft = await metaplex.nfts().findByMint({ mintAddress: mintPublicKey });

//     return {
//         name: nft.name.trim(),
//         symbol: nft.symbol.trim(),
//         decimals: tokenInfo.decimals,
//         supply: tokenInfo.supply.toString(), // Total supply of tokens
//         mintAuthority: tokenInfo.mintAuthority ? tokenInfo.mintAuthority.toBase58() : null,
//     };
// }

// // Function to inspect a list of given token mint addresses
// async function inspectTokenList() {
//     try {
//         console.log(chalk.white.bold('\nInspecting Tokens:\n'));

//         for (let mint of mintAddresses) {
//             // Fetch additional token information using the mint address
//             const { name, symbol, decimals, supply, mintAuthority } = await getTokenInfo(mint);

//             console.log(chalk.cyan(`Mint Address: ${mint}`));
//             console.log(chalk.green(`  Name: ${name}`));
//             console.log(chalk.green(`  Symbol: ${symbol}`));
//             console.log(chalk.green(`  Decimals: ${decimals}`));
//             console.log(chalk.green(`  Total Supply: ${supply}`));
//             // console.log(chalk.yellow(`  Mint Authority: ${mintAuthority || 'None'}`));
//             console.log(chalk.grey('---------------------------------------------'));

//             // Wait for a second before fetching the next token info (to avoid rate limiting)
//             await sleep(2000);
//         }

//     } catch (error) {
//         console.error(chalk.red('Error fetching token info:'), error);
//     }
// }

// // Call the function to inspect the list of tokens
// inspectTokenList();
const fs = require('fs');
const path = require('path');
const chalk = require('chalk');
const solanaWeb3 = require('@solana/web3.js');
const splToken = require('@solana/spl-token');
const { Metaplex, keypairIdentity, bundlrStorage, mockStorage } = require('@metaplex-foundation/js');

// Suppress deprecation warnings
process.noDeprecation = true;

const walletAddress = '6ZDdVLFc2CRaPUwUGnfUsmXr32EBWoNaM9Axf5LWUjc6';
const filePath = path.join(__dirname, 'data', `tokens_${walletAddress}.txt`);
const data = fs.readFileSync(filePath, 'utf8');
const mintAddresses = data.split('\n').filter(line => line.trim() !== '' && line.trim() !== 'So11111111111111111111111111111111111111112'); // Remove SOL address

// Connect to the Solana cluster (Mainnet, Devnet, or Testnet)
const connection = new solanaWeb3.Connection(solanaWeb3.clusterApiUrl('mainnet-beta'), 'confirmed');

// Initialize Metaplex
const metaplex = new Metaplex(connection).use(mockStorage()); // Use mockStorage for simplicity

// Helper function to introduce a delay
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Function to fetch token information based on the mint address
async function getTokenInfo(mintAddress) {
    const mintPublicKey = new solanaWeb3.PublicKey(mintAddress);
    const tokenInfo = await splToken.getMint(connection, mintPublicKey);

    // Fetch metadata using the Metaplex SDK
    const nft = await metaplex.nfts().findByMint({ mintAddress: mintPublicKey });

    return {
        name: nft.name.trim(),
        symbol: nft.symbol.trim(),
        decimals: tokenInfo.decimals,
        supply: tokenInfo.supply.toString(), // Total supply of tokens
        mintAuthority: tokenInfo.mintAuthority ? tokenInfo.mintAuthority.toBase58() : null,
    };
}

// Function to inspect a list of given token mint addresses
async function inspectTokenList() {
    try {
        let output = ''; // Initialize a string to accumulate output

        console.log(chalk.white.bold('\nInspecting Tokens:\n'));

        for (let mint of mintAddresses) {
            // Fetch additional token information using the mint address
            const { name, symbol, decimals, supply, mintAuthority } = await getTokenInfo(mint);

            // Accumulate output
            output += `Mint Address: ${mint}\n`;
            output += `  Name: ${name}\n`;
            output += `  Symbol: ${symbol}\n`;
            output += `  Total Supply: ${supply}\n`;
            output += `---------------------------------------------\n`;

            // Print token details to console
            console.log(chalk.cyan(`Mint Address: ${mint}`));
            console.log(chalk.green(`  Name: ${name}`));
            console.log(chalk.green(`  Symbol: ${symbol}`));
            console.log(chalk.green(`  Total Supply: ${supply}`));
            console.log(chalk.grey('---------------------------------------------'));

            // Wait for a second before fetching the next token info (to avoid rate limiting)
            await sleep(2000);
        }

        // Write output to file
        const outputFilePath = path.join(__dirname, 'data', `token_details_${walletAddress}.txt`);
        fs.writeFileSync(outputFilePath, output, 'utf8');
        console.log(chalk.grey.italic(`Token details have been saved to ${outputFilePath}`));

    } catch (error) {
        console.error(chalk.red('Error fetching token info:'), error);
    }
}

// Call the function to inspect the list of tokens
inspectTokenList();

