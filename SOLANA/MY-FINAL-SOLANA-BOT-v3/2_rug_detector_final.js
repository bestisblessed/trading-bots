const { Connection, PublicKey } = require('@solana/web3.js');
const { getMint } = require('@solana/spl-token');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');
const rugDetectionsDir = './rug-detections/';
const rankingsDir = './rankings/';

console.log('');

async function rugDetector(mint_address) {
    const csvFilePath = path.join(__dirname, 'rug-detections', `${mint_address}.csv`);
    let liquidityUsd = 0;

    if (fs.existsSync(csvFilePath)) {
        const csvData = [];
        await new Promise((resolve, reject) => {
            fs.createReadStream(csvFilePath)
                .pipe(csv())
                .on('data', (row) => {
                    csvData.push(row);
                })
                .on('end', () => {
                    const usdLiquidity = parseFloat(csvData[0]['USD Liquidity']);
                    liquidityUsd = usdLiquidity; // Set the liquidity from the CSV file
                    resolve();
                })
                .on('error', reject);
        });
    } else {
        console.error(`CSV file for ${mint_address} not found.`);
        return; // Exit if the CSV file doesn't exist
    }

    const connection = new Connection('https://api.mainnet-beta.solana.com', 'confirmed');
    const mintPublicKey = new PublicKey(mint_address);
    const mintInfo = await getMint(connection, mintPublicKey);

    if (mintInfo.freezeAuthority) {
        console.log(`FAIL: Token ${mint_address} is freezeable. Freeze Authority: ${mintInfo.freezeAuthority.toBase58()}`);
    } else {
        console.log(`PASS: Token ${mint_address} is not freezeable.`);
    }

    if (mintInfo.mintAuthority) {
        console.log(`FAIL: Token ${mint_address} has a mint authority: ${mintInfo.mintAuthority.toBase58()}`);
    } else {
        console.log(`PASS: Token ${mint_address} does not have a mint authority.`);
    }

    if (!mintInfo.mintAuthority && !mintInfo.freezeAuthority) {
        console.log(`PASS: Token ${mint_address} has renounced ownership (no mint or freeze authority).`);
    } else {
        console.log(`FAIL: Token ${mint_address} has not renounced ownership.`);
    }

    const largestAccounts = await connection.getTokenLargestAccounts(mintPublicKey);

    console.log(`Top holders for token ${mint_address}:`);
    largestAccounts.value.forEach((accountInfo, index) => {
        console.log(`  ${index + 1}. Account: ${accountInfo.address.toBase58()}, Amount: ${accountInfo.uiAmount}`);
    });

    const topHolderThreshold = 50;
    const largestHolder = largestAccounts.value[0];
    if (largestHolder && largestHolder.uiAmount > topHolderThreshold) {
        console.log(`FAIL: Largest holder owns more than ${topHolderThreshold}% of the token supply.`);
    } else {
        console.log(`PASS: No holder owns more than ${topHolderThreshold}% of the token supply.`);
    }

    if (liquidityUsd < 10000) {
        console.log(`FAIL: Token ${mint_address} has low liquidity ($ ${liquidityUsd}).`);
    } else {
        console.log(`PASS: Token ${mint_address} has sufficient liquidity $ ${liquidityUsd}.`);
    }

    const results = {
        mint_address,
        freezeAuthority: mintInfo.freezeAuthority ? mintInfo.freezeAuthority.toBase58() : 'None',
        mintAuthority: mintInfo.mintAuthority ? mintInfo.mintAuthority.toBase58() : 'None',
        ownershipRenounced: !mintInfo.mintAuthority && !mintInfo.freezeAuthority,
        topHolders: largestAccounts.value.map((accountInfo, index) => ({
            rank: index + 1,
            account: accountInfo.address.toBase58(),
            amount: accountInfo.uiAmount,
        })),
        largestHolderPercentage: largestHolder && largestHolder.uiAmount > topHolderThreshold ? largestHolder.uiAmount : 0,
        liquidity: liquidityUsd
    };

    const filePath = path.join(__dirname, 'rug-detections', `${mint_address}.json`);
    try {
        fs.writeFileSync(filePath, JSON.stringify(results, null, 2));
        console.log(`Data saved to ${filePath}`);
    } catch (error) {
        console.error(`Error saving file: ${error}`);
    }
}

// Ranking logic - can be added at the end of the file
if (!fs.existsSync('./rankings/')) {
    fs.mkdirSync('./rankings/');
}

fs.readdir('./rug-detections/', (err, files) => {
    if (err) {
        return console.error('Error reading directory:', err);
    }

    files.forEach(file => {
        if (file.endsWith('.json')) {
            const filePath = path.join('./rug-detections/', file);
            const tokenData = JSON.parse(fs.readFileSync(filePath, 'utf8'));

            // Find the corresponding CSV file with the liquidity values
            const csvFilePath = path.join('./rug-detections/', `${tokenData.mint_address}.csv`);
            if (fs.existsSync(csvFilePath)) {
                const csvData = [];
                fs.createReadStream(csvFilePath)
                    .pipe(csv())
                    .on('data', (row) => {
                        csvData.push(row);
                    })
                    .on('end', () => {
                        // Extract liquidity and other values from the first row of CSV
                        const solanaLiquidity = parseFloat(csvData[0]['Solana Liquidity']);
                        const usdLiquidity = parseFloat(csvData[0]['USD Liquidity']);
                        
                        let rank = 0;

                        // Apply ranking rules with the liquidity data from the CSV
                        if (usdLiquidity < 999) {
                            rank = 1;
                        }

                        if (tokenData.mintAuthority !== 'None' || tokenData.freezeAuthority !== 'None') {
                            rank = 1;
                        }

                        if (usdLiquidity > 10000 && tokenData.ownershipRenounced) {
                            rank = 3;
                        }

                        if (usdLiquidity > 10000 &&
                            tokenData.ownershipRenounced &&
                            tokenData.mintAuthority === 'None' &&
                            tokenData.freezeAuthority === 'None') {
                            rank = 4;
                        }

                        if (usdLiquidity > 10000 &&
                            tokenData.ownershipRenounced &&
                            tokenData.mintAuthority === 'None' &&
                            tokenData.freezeAuthority === 'None' &&
                            tokenData.largestHolderPercentage < 50) {
                            rank = 5;
                        }

                        // Assign a default score if no rules matched
                        if (rank === 0) {
                            rank = 2;  // or any other value you consider appropriate for unmatched tokens
                        }

                        const rankData = {
                            mint_address: tokenData.mint_address,
                            rank: rank,
                            solanaLiquidity,
                            usdLiquidity
                        };

                        const outputFilePath = path.join('./rankings/', `${tokenData.mint_address}_rank.json`);
                        try {
                            fs.writeFileSync(outputFilePath, JSON.stringify(rankData, null, 2));
                            console.log(`Processed ${tokenData.mint_address} and assigned rank ${rank}`);
                            console.log();
                        } catch (error) {
                            console.error(`Error saving rank file for ${tokenData.mint_address}:`, error);
                        }
                    });
            } else {
                console.error(`CSV file for ${tokenData.mint_address} not found.`);
            }
        }
    });
});

// rugDetector('7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr');
// Get the mint address from command-line arguments
const mint_address = process.argv[2];

if (!mint_address) {
    console.error('No mint address provided.');
    process.exit(1);
}

// Run the function with the given mint address
rugDetector(mint_address);