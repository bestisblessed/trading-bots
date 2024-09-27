const { Connection, PublicKey } = require('@solana/web3.js');
const { getMint } = require('@solana/spl-token');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

console.log('');

// Function to fetch liquidity from Dexscreener API
async function getLiquidityInfo(tokenMintAddress) {
    const apiUrl = `https://api.dexscreener.com/latest/dex/tokens/${tokenMintAddress}`;
    
    try {
        const response = await axios.get(apiUrl);
        const data = response.data;

        if (data && data.pairs && data.pairs.length > 0) {
            // Get the first pair from the response
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

    const liquidityUsd = await getLiquidityInfo(tokenMintAddress);
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
        liquidity: liquidityUsd
    };

    const filePath = path.join(__dirname, 'rug-detections', `${tokenMintAddress}.json`);
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
                fs.writeFileSync(outputFilePath, JSON.stringify(rankData, null, 2));
                console.log(`Processed ${tokenData.tokenMintAddress} and assigned rank ${rank}`);
            } catch (error) {
                console.error(`Error saving rank file for ${tokenData.tokenMintAddress}:`, error);
            }
        }
    });
});

// Example usage
rugDetector('FsuuJacQ1K5G7xfQf7dfhEKqtEK5enZKWXtpRuXfA5LC');
// rugDetector('Ag19bdRfrDU4WprGrbN8pJaEP3YbLvbuC9gsnaoJgFKz');
// rugDetector('HidqA4SP1owM2FXGBuypJZxqr8VgoGkcXVZvEr6FZFgy');
// rugDetector('BoFPxed7C7KRrpSovxTwjxE8HeiiyH9qY3kJGpnVRUaL');

