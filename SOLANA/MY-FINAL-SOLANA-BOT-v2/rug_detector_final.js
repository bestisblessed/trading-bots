// const { Connection, PublicKey } = require('@solana/web3.js');
// const { getMint } = require('@solana/spl-token');
// const axios = require('axios');
// const fs = require('fs');
// const path = require('path');

// // Get the mint address from the command-line arguments
// const mintAddress = process.argv[2];

// if (!mintAddress) {
//     console.error("Please provide the mint address as the first argument.");
//     process.exit(1);
// }

// // Define the directory where you want to save the token details
// const directory = './rug-detections-rugcheckxyz';

// // Ensure the directory exists
// if (!fs.existsSync(directory)) {
//     fs.mkdirSync(directory, { recursive: true });
// }

// // Construct the API URL using the mint address
// const url = `https://api.rugcheck.xyz/v1/tokens/${mintAddress}/report/summary`;

// axios.get(url, {
//     headers: {
//         'accept': 'application/json'
//     }
// })
// .then(response => {
//     // Check for success status
//     if (response.status === 200) {
//         const data = response.data; // Get the JSON response
//         console.log(JSON.stringify(data, null, 2));  // Print full data response for debugging

//         // Create the file path with the mint address as the filename
//         const filePath = path.join(directory, `${mintAddress}.json`);

//         // Save the full JSON response to the file
//         fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
//         console.log(`Data saved to file: ${filePath}`);
//     } else {
//         console.log(`Error: ${response.status}`);
//     }
// })
// .catch(error => {
//     console.error(`Error: ${error.response ? error.response.status : error.message}`);
// });


// // // Function to fetch liquidity from Dexscreener API
// // async function getLiquidityInfo(tokenMintAddress) {
// //     const apiUrl = `https://api.dexscreener.com/latest/dex/tokens/${tokenMintAddress}`;
    
// //     try {
// //         const response = await axios.get(apiUrl);
// //         const data = response.data;

// //         if (data && data.pairs && data.pairs.length > 0) {
// //             // Get the first pair from the response
// //             const pair = data.pairs[0];
// //             const liquidity = pair.liquidity ? pair.liquidity.usd : 0;
// //             return liquidity;
// //         } else {
// //             console.log(`No liquidity information found for token ${tokenMintAddress}.`);
// //             return 0;
// //         }
// //     } catch (error) {
// //         console.error(`Error fetching liquidity info: ${error}`);
// //         return 0;
// //     }
// // }
// // Function to fetch liquidity from saved JSON file instead of Dexscreener API
// async function getLiquidityFromFile(tokenMintAddress) {
//     const filePath = path.join('rug-detections-rugcheckxyz', `${tokenMintAddress}.json`);

//     // Check if the file exists
//     if (!fs.existsSync(filePath)) {
//         console.log(`File not found for token ${tokenMintAddress}`);
//         return 0; // Default to 0 liquidity if file doesn't exist
//     }

//     // Read the JSON file
//     const data = fs.readFileSync(filePath, 'utf8');
//     const tokenData = JSON.parse(data);

//     // Find the liquidity information in the risks array
//     const liquidityRisk = tokenData.risks.find(risk => risk.name === 'Low Liquidity');

//     if (liquidityRisk && liquidityRisk.value) {
//         const liquidityValue = parseFloat(liquidityRisk.value.replace('$', '')); // Remove the dollar sign and parse it as a float
//         console.log(`Liquidity for token ${tokenMintAddress}: $${liquidityValue}`);
//         return liquidityValue;
//     } else {
//         console.log(`No liquidity information found for token ${tokenMintAddress}`);
//         return 0; // Default to 0 if no liquidity info found
//     }
// }

// async function rugDetector(tokenMintAddress) {
//     const connection = new Connection('https://api.mainnet-beta.solana.com', 'confirmed');
//     let mintPublicKey;

//     try {
//         mintPublicKey = new PublicKey(tokenMintAddress);
//     } catch (error) {
//         console.error(`Invalid mint address provided: ${tokenMintAddress}`);
//         return;
//     }

//     let mintInfo;
//     try {
//         mintInfo = await getMint(connection, mintPublicKey);
//     } catch (error) {
//         console.error(`Error fetching mint info for ${tokenMintAddress}: ${error}`);
//         return;
//     }

//     if (mintInfo.freezeAuthority) {
//         console.log(`FAIL: Token ${tokenMintAddress} is freezeable. Freeze Authority: ${mintInfo.freezeAuthority.toBase58()}`);
//     } else {
//         console.log(`PASS: Token ${tokenMintAddress} is not freezeable.`);
//     }

//     if (mintInfo.mintAuthority) {
//         console.log(`FAIL: Token ${tokenMintAddress} has a mint authority: ${mintInfo.mintAuthority.toBase58()}`);
//     } else {
//         console.log(`PASS: Token ${tokenMintAddress} does not have a mint authority.`);
//     }

//     if (!mintInfo.mintAuthority && !mintInfo.freezeAuthority) {
//         console.log(`PASS: Token ${tokenMintAddress} has renounced ownership (no mint or freeze authority).`);
//     } else {
//         console.log(`FAIL: Token ${tokenMintAddress} has not renounced ownership.`);
//     }

//     let largestAccounts;
//     try {
//         largestAccounts = await connection.getTokenLargestAccounts(mintPublicKey);
//     } catch (error) {
//         console.error(`Error fetching largest accounts for ${tokenMintAddress}: ${error}`);
//         return;
//     }

//     console.log(`Top holders for token ${tokenMintAddress}:`);
//     largestAccounts.value.forEach((accountInfo, index) => {
//         console.log(`  ${index + 1}. Account: ${accountInfo.address.toBase58()}, Amount: ${accountInfo.uiAmount}`);
//     });

//     const topHolderThreshold = 60;
//     const largestHolder = largestAccounts.value[0];
//     if (largestHolder && largestHolder.uiAmount > topHolderThreshold) {
//         console.log(`FAIL: Largest holder owns more than ${topHolderThreshold}% of the token supply.`);
//     } else {
//         console.log(`PASS: No holder owns more than ${topHolderThreshold}% of the token supply.`);
//     }

//     // const liquidity = await getLiquidityInfo(tokenMintAddress);
//     const liquidity = await getLiquidityFromFile(tokenMintAddress);
//     if (liquidity < 10000) {
//         console.log(`FAIL: Token ${tokenMintAddress} has low liquidity ($${liquidity}).`);
//     } else {
//         console.log(`PASS: Token ${tokenMintAddress} has sufficient liquidity $${liquidity}.`);
//     }

//     const results = {
//         tokenMintAddress,
//         freezeAuthority: mintInfo.freezeAuthority ? mintInfo.freezeAuthority.toBase58() : 'None',
//         mintAuthority: mintInfo.mintAuthority ? mintInfo.mintAuthority.toBase58() : 'None',
//         ownershipRenounced: !mintInfo.mintAuthority && !mintInfo.freezeAuthority,
//         topHolders: largestAccounts.value.map((accountInfo, index) => ({
//             rank: index + 1,
//             account: accountInfo.address.toBase58(),
//             amount: accountInfo.uiAmount,
//         })),
//         largestHolderPercentage: largestHolder && largestHolder.uiAmount > topHolderThreshold ? largestHolder.uiAmount : 0,
//         liquidity: liquidity
//     };

//     const filePath = path.join(__dirname, 'rug-detections', `${tokenMintAddress}.json`);
//     try {
//         // Ensure the output directory exists
//         if (!fs.existsSync(path.join(__dirname, 'rug-detections'))) {
//             fs.mkdirSync(path.join(__dirname, 'rug-detections'), { recursive: true });
//             console.log(`Created directory: ${path.join(__dirname, 'rug-detections')}`);
//         }

//         fs.writeFileSync(filePath, JSON.stringify(results, null, 2));
//         console.log(`Data saved to ${filePath}`);
//     } catch (error) {
//         console.error(`Error saving file: ${error}`);
//     }
// }

// // Function to assign rank based on token data
// function assignRank(tokenData) {
//     let rank = 0;

//     // Apply ranking rules
//     if (tokenData.liquidity < 999) {
//         rank = 1;
//     }

//     if (tokenData.mintAuthority !== 'None' || tokenData.freezeAuthority !== 'None') {
//         rank = 1;
//     }

//     if (tokenData.liquidity > 10000 && tokenData.ownershipRenounced) {
//         rank = 3;
//     }
    
//     if (tokenData.liquidity > 10000 &&
//         tokenData.ownershipRenounced &&
//         tokenData.mintAuthority === 'None' &&
//         tokenData.freezeAuthority === 'None') {
//         rank = 4;
//     }

//     if (tokenData.liquidity > 10000 &&
//         tokenData.ownershipRenounced &&
//         tokenData.mintAuthority === 'None' &&
//         tokenData.freezeAuthority === 'None' &&
//         tokenData.largestHolderPercentage < 60) {
//         rank = 5;
//     }

//     // Assign a default score if no rules matched
//     if (rank === 0) {
//         rank = 2;  // or any other value you consider appropriate for unmatched tokens
//     }

//     return rank;
// }

// // Ranking logic
// function processRankings() {
//     const rankingsDir = path.join(__dirname, 'rankings');
//     const detectionsDir = path.join(__dirname, 'rug-detections');

//     // Ensure the rankings directory exists
//     if (!fs.existsSync(rankingsDir)) {
//         fs.mkdirSync(rankingsDir, { recursive: true });
//         console.log(`Created directory: ${rankingsDir}`);
//     }

//     fs.readdir(detectionsDir, (err, files) => {
//         if (err) {
//             return console.error('Error reading detections directory:', err.message);
//         }

//         files.forEach(file => {
//             if (file.endsWith('.json')) {
//                 const tokenMintAddress = path.basename(file, '.json');
//                 const rankFilePath = path.join(rankingsDir, `${tokenMintAddress}_rank.json`);

//                 // Check if rank file already exists
//                 if (fs.existsSync(rankFilePath)) {
//                     // console.log(`Rank file already exists for token ${tokenMintAddress}. Skipping ranking.`);
//                     return;
//                 }

//                 const filePath = path.join(detectionsDir, file);
//                 let tokenData;
//                 try {
//                     const rawData = fs.readFileSync(filePath, 'utf8');
//                     tokenData = JSON.parse(rawData);
//                 } catch (error) {
//                     return console.error(`Error reading or parsing ${filePath}:`, error.message);
//                 }

//                 const rank = assignRank(tokenData);

//                 const rankData = {
//                     tokenMintAddress: tokenData.tokenMintAddress,
//                     rank: rank
//                 };

//                 try {
//                     fs.writeFileSync(rankFilePath, JSON.stringify(rankData, null, 2));
//                     console.log(`Processed ${tokenMintAddress} and assigned rank ${rank}`);
//                 } catch (error) {
//                     console.error(`Error saving rank file for ${tokenMintAddress}:`, error.message);
//                 }
//             }
//         });
//     });
// }

// // Parse command-line arguments
// const args = process.argv.slice(2);
// if (args.length < 1) {
//     console.error('Usage: node rugcheckxyz.js <TokenMintAddress>');
//     process.exit(1);
// }

// const tokenMintAddress = args[0];

// // Execute the rug detection and ranking
// rugDetector(tokenMintAddress).then(() => {
//     // After rug detection, process rankings
//     processRankings();
// });

// // Example usage
// // rugDetector('Ag19bdRfrDU4WprGrbN8pJaEP3YbLvbuC9gsnaoJgFKz');
// // rugDetector('HidqA4SP1owM2FXGBuypJZxqr8VgoGkcXVZvEr6FZFgy');
// // rugDetector('BoFPxed7C7KRrpSovxTwjxE8HeiiyH9qY3kJGpnVRUaL');
const { Connection, PublicKey } = require('@solana/web3.js');
const { getMint } = require('@solana/spl-token');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

// Get the mint address from the command-line arguments
const mintAddress = process.argv[2];

if (!mintAddress) {
    console.error("Please provide the mint address as the first argument.");
    process.exit(1);
}

// Define the directory where you want to save the token details
const directory = './rug-detections-rugcheckxyz';

// Ensure the directory exists
if (!fs.existsSync(directory)) {
    fs.mkdirSync(directory, { recursive: true });
}

// Construct the API URL using the mint address
const url = `https://api.rugcheck.xyz/v1/tokens/${mintAddress}/report/summary`;

async function runRugCheckAPI() {
    try {
        const response = await axios.get(url, {
            headers: { 'accept': 'application/json' }
        });

        if (response.status === 200) {
            const data = response.data;
            console.log(JSON.stringify(data, null, 2));

            // Create the file path with the mint address as the filename
            const filePath = path.join(directory, `${mintAddress}.json`);

            // Save the full JSON response to the file
            fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
            console.log(`Data saved to file: ${filePath}`);
        } else {
            console.log(`Error: ${response.status}`);
        }
    } catch (error) {
        console.error(`Error: ${error.response ? error.response.status : error.message}`);
    }
}

// Function to fetch liquidity from saved JSON file instead of Dexscreener API
async function getLiquidityFromFile(tokenMintAddress) {
    const filePath = path.join('rug-detections-rugcheckxyz', `${tokenMintAddress}.json`);

    // Check if the file exists
    if (!fs.existsSync(filePath)) {
        console.log(`File not found for token ${tokenMintAddress}`);
        return 0; // Default to 0 liquidity if file doesn't exist
    }

    // Read the JSON file
    const data = fs.readFileSync(filePath, 'utf8');
    const tokenData = JSON.parse(data);

    // Find the liquidity information in the risks array
    const liquidityRisk = tokenData.risks.find(risk => risk.name === 'Low Liquidity');

    if (liquidityRisk && liquidityRisk.value) {
        const liquidityValue = parseFloat(liquidityRisk.value.replace('$', '')); // Remove the dollar sign and parse it as a float
        console.log(`Liquidity for token ${tokenMintAddress}: $${liquidityValue}`);
        return liquidityValue;
    } else {
        console.log(`No liquidity information found for token ${tokenMintAddress}`);
        return 0; // Default to 0 if no liquidity info found
    }
}

async function rugDetector(tokenMintAddress) {
    const connection = new Connection('https://api.mainnet-beta.solana.com', 'confirmed');
    let mintPublicKey;

    try {
        mintPublicKey = new PublicKey(tokenMintAddress);
    } catch (error) {
        console.error(`Invalid mint address provided: ${tokenMintAddress}`);
        return;
    }

    let mintInfo;
    try {
        mintInfo = await getMint(connection, mintPublicKey);
    } catch (error) {
        console.error(`Error fetching mint info for ${tokenMintAddress}: ${error}`);
        return;
    }

    if (mintInfo.freezeAuthority) {
        console.log(`FAIL: Token ${tokenMintAddress} is freezeable. Freeze Authority: ${mintInfo.freezeAuthority.toBase58()}`);
    } else {
        console.log(`PASS: Token ${tokenMintAddress} is not freezeable.`);
    }

    if (mintInfo.mintAuthority) {
        console.log(`FAIL: Token ${tokenMintAddress} has a mint authority: ${mintInfo.mintAuthority.toBase58()}`);
    } else {
        console.log(`PASS: Token ${tokenMintAddress} does not have a mint authority.`);
    }

    if (!mintInfo.mintAuthority && !mintInfo.freezeAuthority) {
        console.log(`PASS: Token ${tokenMintAddress} has renounced ownership (no mint or freeze authority).`);
    } else {
        console.log(`FAIL: Token ${tokenMintAddress} has not renounced ownership.`);
    }

    let largestAccounts;
    try {
        largestAccounts = await connection.getTokenLargestAccounts(mintPublicKey);
    } catch (error) {
        console.error(`Error fetching largest accounts for ${tokenMintAddress}: ${error}`);
        return;
    }

    console.log(`Top holders for token ${tokenMintAddress}:`);
    largestAccounts.value.forEach((accountInfo, index) => {
        console.log(`  ${index + 1}. Account: ${accountInfo.address.toBase58()}, Amount: ${accountInfo.uiAmount}`);
    });

    const topHolderThreshold = 60;
    const largestHolder = largestAccounts.value[0];
    if (largestHolder && largestHolder.uiAmount > topHolderThreshold) {
        console.log(`FAIL: Largest holder owns more than ${topHolderThreshold}% of the token supply.`);
    } else {
        console.log(`PASS: No holder owns more than ${topHolderThreshold}% of the token supply.`);
    }

    // Fetch liquidity from the saved file
    const liquidity = await getLiquidityFromFile(tokenMintAddress);
    if (liquidity < 10000) {
        console.log(`FAIL: Token ${tokenMintAddress} has low liquidity ($${liquidity}).`);
    } else {
        console.log(`PASS: Token ${tokenMintAddress} has sufficient liquidity $${liquidity}.`);
    }

    const results = {
        tokenMintAddress,
        freezeAuthority: mintInfo.freezeAuthority ? mintInfo.freezeAuthority.toBase58() : 'None',
        mintAuthority: mintInfo.mintAuthority ? mintInfo.mintAuthority.toBase58() : 'None',
        ownershipRenounced: !mintInfo.mintAuthority && !mintInfo.freezeAuthority,
        topHolders: largestAccounts.value.map((accountInfo, index) => ({
            rank: index + 1,
            account: accountInfo.address.toBase58(),
            amount: accountInfo.uiAmount,
        })),
        largestHolderPercentage: largestHolder && largestHolder.uiAmount > topHolderThreshold ? largestHolder.uiAmount : 0,
        liquidity: liquidity
    };

    const filePath = path.join(__dirname, 'rug-detections', `${tokenMintAddress}.json`);
    try {
        // Ensure the output directory exists
        if (!fs.existsSync(path.join(__dirname, 'rug-detections'))) {
            fs.mkdirSync(path.join(__dirname, 'rug-detections'), { recursive: true });
            console.log(`Created directory: ${path.join(__dirname, 'rug-detections')}`);
        }

        fs.writeFileSync(filePath, JSON.stringify(results, null, 2));
        console.log(`Data saved to ${filePath}`);
    } catch (error) {
        console.error(`Error saving file: ${error}`);
    }
}

// Function to assign rank based on token data
function assignRank(tokenData) {
    let rank = 0;

    // Apply ranking rules
    if (tokenData.liquidity < 999) {
        rank = 1;
    }

    if (tokenData.mintAuthority !== 'None' || tokenData.freezeAuthority !== 'None') {
        rank = 1;
    }

    if (tokenData.liquidity > 10000 && tokenData.ownershipRenounced) {
        rank = 3;
    }
    
    if (tokenData.liquidity > 10000 &&
        tokenData.ownershipRenounced &&
        tokenData.mintAuthority === 'None' &&
        tokenData.freezeAuthority === 'None') {
        rank = 4;
    }

    if (tokenData.liquidity > 10000 &&
        tokenData.ownershipRenounced &&
        tokenData.mintAuthority === 'None' &&
        tokenData.freezeAuthority === 'None' &&
        tokenData.largestHolderPercentage < 60) {
        rank = 5;
    }

    // Assign a default score if no rules matched
    if (rank === 0) {
        rank = 2;  // or any other value you consider appropriate for unmatched tokens
    }

    return rank;
}

// Ranking logic
function processRankings() {
    const rankingsDir = path.join(__dirname, 'rankings');
    const detectionsDir = path.join(__dirname, 'rug-detections');

    // Ensure the rankings directory exists
    if (!fs.existsSync(rankingsDir)) {
        fs.mkdirSync(rankingsDir, { recursive: true });
        console.log(`Created directory: ${rankingsDir}`);
    }

    fs.readdir(detectionsDir, (err, files) => {
        if (err) {
            return console.error('Error reading detections directory:', err.message);
        }

        files.forEach(file => {
            if (file.endsWith('.json')) {
                const tokenMintAddress = path.basename(file, '.json');
                const rankFilePath = path.join(rankingsDir, `${tokenMintAddress}_rank.json`);

                // Check if rank file already exists
                if (fs.existsSync(rankFilePath)) {
                    // console.log(`Rank file already exists for token ${tokenMintAddress}. Skipping ranking.`);
                    return;
                }

                const filePath = path.join(detectionsDir, file);
                let tokenData;
                try {
                    const rawData = fs.readFileSync(filePath, 'utf8');
                    tokenData = JSON.parse(rawData);
                } catch (error) {
                    return console.error(`Error reading or parsing ${filePath}:`, error.message);
                }

                const rank = assignRank(tokenData);

                const rankData = {
                    tokenMintAddress: tokenData.tokenMintAddress,
                    rank: rank
                };

                try {
                    fs.writeFileSync(rankFilePath, JSON.stringify(rankData, null, 2));
                    console.log(`Processed ${tokenMintAddress} and assigned rank ${rank}`);
                } catch (error) {
                    console.error(`Error saving rank file for ${tokenMintAddress}:`, error.message);
                }
            }
        });
    });
}

// Execute RugCheck API, then run rugDetector once data is saved
async function run() {
    await runRugCheckAPI();
    await rugDetector(mintAddress);
}

run().then(() => {
    // After rug detection, process rankings or any further logic
    processRankings();
});

// // Execute RugCheck API, then run rugDetector once data is saved
// async function run() {
//     await runRugCheckAPI();
//     await rugDetector(mintAddress);
// }

// run().then(() => {
//     // After rug detection, process rankings or any further logic
// });
