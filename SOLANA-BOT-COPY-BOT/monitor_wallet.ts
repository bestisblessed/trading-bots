// import { Connection, PublicKey } from "@solana/web3.js";
// import * as fs from 'fs';
// import * as path from 'path';

// interface TokenData {
//   index: number;
//   mint: string;
//   owner: string;
//   programId: string;
//   amount: string;
//   decimals: number;
//   uiAmountString: string;
// }

// async function getTokenBalances(walletAddress: string) {
//   // Initialize a connection to the Solana RPC endpoint
//   const connection = new Connection("https://api.mainnet-beta.solana.com");

//   try {
//     // Convert wallet address to PublicKey
//     const publicKey = new PublicKey(walletAddress);

//     // Fetch token accounts by owner
//     const tokenAccounts = await connection.getParsedTokenAccountsByOwner(publicKey, {
//       programId: new PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA") // Token Program ID
//     });

//     console.log(`Monitoring: ${walletAddress}...`);

//     const tokensData: TokenData[] = [];
    
//     // Iterate through token accounts and collect details
//     tokenAccounts.value.forEach((tokenAccount, index) => {
//       const accountInfo = tokenAccount.account.data.parsed.info;
//       const tokenAmount = accountInfo.tokenAmount;

//       const tokenData: TokenData = {
//         index: index + 1,
//         mint: accountInfo.mint,
//         owner: accountInfo.owner,
//         programId: tokenAccount.account.owner.toString(),
//         amount: tokenAmount.amount,
//         decimals: tokenAmount.decimals,
//         uiAmountString: tokenAmount.uiAmountString,
//       };
    
//       // Push the token data to the array
//       tokensData.push(tokenData);
//     });

//     // Ensure the data/ directory exists
//     const dataDir = path.join(__dirname, 'data');
//     if (!fs.existsSync(dataDir)) {
//       fs.mkdirSync(dataDir);
//     }

//     // Define the path for the output file
//     const outputPath = path.join(dataDir, `${walletAddress}_token_balances.json`);
//     const updatesPath = path.join(dataDir, `updated_tokens.json`);

//     // Check if the previous file exists
//     let previousData: TokenData[] = [];
//     if (fs.existsSync(outputPath)) {
//       const rawData = fs.readFileSync(outputPath, 'utf-8');
//       previousData = JSON.parse(rawData);
//     }

//     // Compare previous and current data
//     const previousMints = new Set(previousData.map(token => token.mint));
//     const currentMints = new Set(tokensData.map(token => token.mint));

//     const addedTokens = tokensData.filter(token => !previousMints.has(token.mint));
//     const removedTokens = previousData.filter(token => !currentMints.has(token.mint));

//     if (addedTokens.length > 0 || removedTokens.length > 0) {
//       const updatedTokens = {
//         added: addedTokens,
//         removed: removedTokens,
//       };

//       if (addedTokens.length > 0) {
//         console.log('\nNEW TOKENS ADDED:');
//         addedTokens.forEach(token => {
//           console.log(`  Mint: ${token.mint}`);
//           console.log(`  Amount: ${token.amount}`);
//           console.log("");
//         });
//       }

//       if (removedTokens.length > 0) {
//         console.log('\nTOKENS REMOVED:');
//         removedTokens.forEach(token => {
//           console.log(`  Mint: ${token.mint}`);
//           console.log(`  Amount: ${token.amount}`);
//           console.log("");
//         });
//       }

//       // Save the updated tokens to a separate JSON file
//       fs.writeFileSync(updatesPath, JSON.stringify(updatedTokens, null, 2));
//       console.log(`Updated tokens saved to ${updatesPath}`);
//     }

//     // Write the token data to a JSON file
//     fs.writeFileSync(outputPath, JSON.stringify(tokensData, null, 2));

//   } catch (error) {
//     console.error("Failed to fetch token balances:", error);
//   }
// }

// // Example usage: Pass the wallet address as a command-line argument
// const walletAddress = process.argv[2];
// if (!walletAddress) {
//   console.error("Please provide a wallet address as an argument.");
//   process.exit(1);
// }

// getTokenBalances(walletAddress);
import { Connection, PublicKey } from "@solana/web3.js";
import * as fs from 'fs';
import * as path from 'path';

interface TokenData {
  index: number;
  mint: string;
  owner: string;
  programId: string;
  amount: string;
  decimals: number;
  uiAmountString: string;
}

async function getTokenBalances(walletAddress: string) {
  // Initialize a connection to the Solana RPC endpoint
  const connection = new Connection("https://api.mainnet-beta.solana.com");

  try {
    // Convert wallet address to PublicKey
    const publicKey = new PublicKey(walletAddress);

    // Fetch token accounts by owner
    const tokenAccounts = await connection.getParsedTokenAccountsByOwner(publicKey, {
      programId: new PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA") // Token Program ID
    });

    console.log(`Monitoring: ${walletAddress}...`);

    const tokensData: TokenData[] = [];
    
    // Iterate through token accounts and collect details
    tokenAccounts.value.forEach((tokenAccount, index) => {
      const accountInfo = tokenAccount.account.data.parsed.info;
      const tokenAmount = accountInfo.tokenAmount;

      const tokenData: TokenData = {
        index: index + 1,
        mint: accountInfo.mint,
        owner: accountInfo.owner,
        programId: tokenAccount.account.owner.toString(),
        amount: tokenAmount.amount,
        decimals: tokenAmount.decimals,
        uiAmountString: tokenAmount.uiAmountString,
      };
    
      // Push the token data to the array
      tokensData.push(tokenData);
    });

    // Ensure the data/ directory exists
    const dataDir = path.join(__dirname, 'data');
    if (!fs.existsSync(dataDir)) {
      fs.mkdirSync(dataDir);
    }

    // Define the path for the output file
    const outputPath = path.join(dataDir, `${walletAddress}_token_balances.json`);
    const updatesPath = path.join(dataDir, `updated_tokens.json`);

    // Check if the previous file exists
    let previousData: TokenData[] = [];
    if (fs.existsSync(outputPath)) {
      const rawData = fs.readFileSync(outputPath, 'utf-8');
      previousData = JSON.parse(rawData);
    }

    // Compare previous and current data
    const previousMints = new Set(previousData.map(token => token.mint));
    const currentMints = new Set(tokensData.map(token => token.mint));

    const addedTokens = tokensData.filter(token => !previousMints.has(token.mint));
    const removedTokens = previousData.filter(token => !currentMints.has(token.mint));

    // Create updated_tokens.json if tokens are added or removed
    if (addedTokens.length > 0 || removedTokens.length > 0) {
      const updatedTokens = {
        added: addedTokens,
        removed: removedTokens,
      };

      if (addedTokens.length > 0) {
        console.log('\nNEW TOKENS ADDED:');
        addedTokens.forEach(token => {
          console.log(`  Mint: ${token.mint}`);
          console.log(`  Amount: ${token.amount}`);
          console.log("");
        });
      }

      if (removedTokens.length > 0) {
        console.log('\nTOKENS REMOVED:');
        removedTokens.forEach(token => {
          console.log(`  Mint: ${token.mint}`);
          console.log(`  Amount: ${token.amount}`);
          console.log("");
        });
      }

      // Save the updated tokens to a separate JSON file
      fs.writeFileSync(updatesPath, JSON.stringify(updatedTokens, null, 2));
      console.log(`Updated tokens saved to ${updatesPath}`);
    } else {
      console.log("No tokens added or removed, not creating updated_tokens.json");
    }

    // Write the current token data to the balances file
    fs.writeFileSync(outputPath, JSON.stringify(tokensData, null, 2));

  } catch (error) {
    console.error("Failed to fetch token balances:", error);
  }
}

// Example usage: Pass the wallet address as a command-line argument
const walletAddress = process.argv[2];
if (!walletAddress) {
  console.error("Please provide a wallet address as an argument.");
  process.exit(1);
}

getTokenBalances(walletAddress);
