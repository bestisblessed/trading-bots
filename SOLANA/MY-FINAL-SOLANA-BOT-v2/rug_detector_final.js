const { Connection, PublicKey } = require('@solana/web3.js');
const { getMint } = require('@solana/spl-token');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
console.log('');

// Get the mint address from the command-line arguments
const tokenMintAddress = process.argv[2];
if (!tokenMintAddress) {
    console.error("No mint address provided!");
    process.exit(1);
}

// Function to fetch liquidity from Dexscreener API
async function getLiquidityInfo(tokenMintAddress) {
    const apiUrl = `https://api.dexscreener.com/latest/dex/tokens/${tokenMintAddress}`;
    
    try {
        const response = await axios.get(apiUrl);
        const data = response.data;

        if (data && data.pairs && data.pairs.length > 0) {
            const pair = data.pairs[0];
            const liquidityUsd = pair.liquidity ? pair.liquidity.usd : 0;
            return liquidityUsd;
        } else {
            console.log(`No liquidity information found for token ${tokenMintAddress}.`);
            return 0;
        }
    } catch (error) {
        console.error(`Error fetching liquidity info: ${error}`);
        return 0;
    }
}

async function rugDetector(tokenMintAddress) {
    const connection = new Connection('https://api.mainnet-beta.solana.com', 'confirmed');
    const mintPublicKey = new PublicKey(tokenMintAddress);
    
    // Fetch liquidity first
    const liquidityUsd = await getLiquidityInfo(tokenMintAddress);

    const mintInfo = await getMint(connection, mintPublicKey);

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

    const largestAccounts = await connection.getTokenLargestAccounts(mintPublicKey);
    console.log(`Top holders for token ${tokenMintAddress}:`);
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
        console.log(`FAIL: Token ${tokenMintAddress} has low liquidity ($${liquidityUsd}).`);
    } else {
        console.log(`PASS: Token ${tokenMintAddress} has sufficient liquidity $${liquidityUsd}.`);
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
        liquidity: liquidityUsd // Include liquidity in the results
    };

    const filePath = path.join(__dirname, 'rug-detections', `${tokenMintAddress}.json`);
    try {
        fs.writeFileSync(filePath, JSON.stringify(results, null, 2));
        console.log(`Data saved to ${filePath}`);
    } catch (error) {
        console.error(`Error saving file: ${error}`);
    }

    return results; // Return the results for ranking
}

// Function to handle ranking logic for a specific token
async function rankTokens(tokenData) {
    if (!fs.existsSync('./rankings/')) {
        fs.mkdirSync('./rankings/');
    }

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
        tokenData.largestHolderPercentage < 50) {
        rank = 5;
    }

    // Assign a default score if no rules matched
    if (rank === 0) {
        rank = 2;  // or any other value you consider appropriate for unmatched tokens
    }

    const rankData = {
        tokenMintAddress: tokenData.tokenMintAddress,
        rank: rank
    };

    const outputFilePath = path.join('./rankings/', `${tokenData.tokenMintAddress}_rank.json`);
    try {
        await fs.promises.writeFile(outputFilePath, JSON.stringify(rankData, null, 2)); // Async write
        console.log(`Processed ${tokenData.tokenMintAddress} and assigned rank ${rank}`);
    } catch (error) {
        console.error(`Error saving rank file for ${tokenData.tokenMintAddress}:`, error);
    }
}

// Run the rug detector
// rugDetector(tokenMintAddress).then(() => {
//     // After rug detection, run ranking
//     return rankTokens();
// }).catch(console.error);
rugDetector(tokenMintAddress).then(async (results) => {
    // After rug detection, run ranking for the specific token
    await rankTokens(results); // Pass the results which include liquidity
}).catch(console.error);
