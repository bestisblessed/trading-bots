const { Connection, PublicKey } = require('@solana/web3.js');
const { getMint } = require('@solana/spl-token');
const axios = require('axios');

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
            // console.log(`Liquidity for ${tokenMintAddress}: $${liquidityUsd}`);
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
    // Connect to the Solana cluster
    const connection = new Connection('https://api.mainnet-beta.solana.com', 'confirmed');
    
    // Create a PublicKey object for the token mint address
    const mintPublicKey = new PublicKey(tokenMintAddress);
    
    // Fetch the mint information
    const mintInfo = await getMint(connection, mintPublicKey);
    
    // Check the freeze authority
    if (mintInfo.freezeAuthority) {
        console.log(`FAIL: Token ${tokenMintAddress} is freezeable. Freeze Authority: ${mintInfo.freezeAuthority.toBase58()}`);
    } else {
        console.log(`PASS: Token ${tokenMintAddress} is not freezeable.`);
    }

    // Check the mint authority
    if (mintInfo.mintAuthority) {
        console.log(`FAIL: Token ${tokenMintAddress} has a mint authority: ${mintInfo.mintAuthority.toBase58()}`);
    } else {
        console.log(`PASS: Token ${tokenMintAddress} does not have a mint authority.`);
    }

    // Check for ownership renouncement
    if (!mintInfo.mintAuthority && !mintInfo.freezeAuthority) {
        console.log(`PASS: Token ${tokenMintAddress} has renounced ownership (no mint or freeze authority).`);
    } else {
        console.log(`FAIL: Token ${tokenMintAddress} has not renounced ownership.`);
    }

    // Fetch top holders for the token
    const largestAccounts = await connection.getTokenLargestAccounts(mintPublicKey);

    console.log(`Top holders for token ${tokenMintAddress}:`);
    largestAccounts.value.forEach((accountInfo, index) => {
        console.log(`  ${index + 1}. Account: ${accountInfo.address.toBase58()}, Amount: ${accountInfo.uiAmount}`);
    });

    // If the top holders own a large portion of the supply, it could be a risk
    const topHolderThreshold = 50; // Example: if any holder owns more than 50% of the supply
    const largestHolder = largestAccounts.value[0];
    if (largestHolder && largestHolder.uiAmount > topHolderThreshold) {
        console.log(`FAIL: Largest holder owns more than ${topHolderThreshold}% of the token supply.`);
    } else {
        console.log(`PASS: No holder owns more than ${topHolderThreshold}% of the token supply.`);
    }

    // Fetch liquidity information
    const liquidityUsd = await getLiquidityInfo(tokenMintAddress);
    if (liquidityUsd < 10000) {
        console.log(`FAIL: Token ${tokenMintAddress} has low liquidity ($${liquidityUsd}).`);
    } else {
        console.log(`PASS: Token ${tokenMintAddress} has sufficient liquidity $${liquidityUsd}.`);
    }

}






// Example usage
// rugDetector('HidqA4SP1owM2FXGBuypJZxqr8VgoGkcXVZvEr6FZFgy');
rugDetector('2TVjXHnvRJ9mFS8K9jKQE7ThYjm6NQvh5f66ijECjaUE');
// rugDetector('7QtA5Bg4eLtVbD7X7oDohxuRqzN9mRkuFoXKpoHdhQ1h');
