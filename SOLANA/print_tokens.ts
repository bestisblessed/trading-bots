import { Connection, PublicKey } from '@solana/web3.js';
import { TOKEN_PROGRAM_ID, getAccount, getMint } from '@solana/spl-token';
import { connection, owner } from './config'; // Assumes your connection and owner are set up in config.ts
import * as fs from 'fs'; // Import the 'fs' module for file operations

// Helper function to create a delay (2 seconds in this case)
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

const printTokens = async () => {
  try {
    // Fetch all token accounts owned by the wallet
    const tokenAccounts = await connection.getTokenAccountsByOwner(
      owner.publicKey,
      { programId: TOKEN_PROGRAM_ID }
    );

    // Create a writable stream to save the output to a file
    const walletAddress = owner.publicKey.toBase58();
    // const outputStream = fs.createWriteStream(`data/${walletAddress}.txt`, { flags: 'w' }); // 'w' flag to append
    const outputFilePath = `data/${walletAddress}.json`;
    let tokenDataArray: any[] = []; // Array to hold token account details

    console.log('');
    console.log(`Found ${tokenAccounts.value.length} token accounts for wallet ${owner.publicKey.toBase58()}:`);
    console.log('------------------------');

    // Iterate over each token account and print details with a 2-second delay
    for (const { pubkey, account } of tokenAccounts.value) {
      const tokenAccount = await getAccount(connection, pubkey);
      const mintAddress = tokenAccount.mint.toBase58();

      // Fetch the token mint info to get the decimals
      const mintInfo = await getMint(connection, tokenAccount.mint);
      const decimals = mintInfo.decimals;

      // Calculate the token balance based on decimals
      const tokenBalance = Number(tokenAccount.amount) / Math.pow(10, decimals);

      // Print token details
      console.log(`Token Account: ${pubkey.toBase58()}`);
      console.log(`Mint Address: ${mintAddress}`);
      console.log(`Token Balance: ${tokenBalance}`);
      console.log(`Decimals: ${decimals}`);
      console.log(`Is Initialized: ${tokenAccount.isInitialized}`);
      console.log(`Is Frozen: ${tokenAccount.isFrozen}`);
      if (tokenAccount.delegate) {
        console.log(`Delegate: ${tokenAccount.delegate.toBase58()}`);
        console.log(`Delegated Amount: ${tokenAccount.delegatedAmount.toString()}`);
      } else {
        console.log('No Delegate assigned');
      }
      if (tokenAccount.closeAuthority) {
        console.log(`Close Authority: ${tokenAccount.closeAuthority.toBase58()}`);
      } else {
        console.log('No Close Authority');
      }
      console.log(`Total Supply: ${Number(mintInfo.supply) / Math.pow(10, decimals)}`);
      console.log(`Mint Authority: ${mintInfo.mintAuthority ? mintInfo.mintAuthority.toBase58() : 'None'}`);
      console.log(`Freeze Authority: ${mintInfo.freezeAuthority ? mintInfo.freezeAuthority.toBase58() : 'None'}`);
      console.log(`Mint is Initialized: ${mintInfo.isInitialized}`);
      console.log('------------------------');

    //   // Write token details to the file
    //   outputStream.write(`Token Account: ${pubkey.toBase58()}\n`);
    //   outputStream.write(`Mint Address: ${mintAddress}\n`);
    //   outputStream.write(`Token Balance: ${tokenBalance}\n`);
    //   outputStream.write(`Decimals: ${decimals}\n`);
    //   outputStream.write(`Is Initialized: ${tokenAccount.isInitialized}\n`);
    //   outputStream.write(`Is Frozen: ${tokenAccount.isFrozen}\n`);
    //   if (tokenAccount.delegate) {
    //     outputStream.write(`Delegate: ${tokenAccount.delegate.toBase58()}\n`);
    //     outputStream.write(`Delegated Amount: ${tokenAccount.delegatedAmount.toString()}\n`);
    //   } else {
    //     outputStream.write('No Delegate assigned\n');
    //   }
    //   if (tokenAccount.closeAuthority) {
    //     outputStream.write(`Close Authority: ${tokenAccount.closeAuthority.toBase58()}\n`);
    //   } else {
    //     outputStream.write('No Close Authority\n');
    //   }
    //   outputStream.write(`Total Supply: ${Number(mintInfo.supply) / Math.pow(10, decimals)}\n`);
    //   outputStream.write(`Mint Authority: ${mintInfo.mintAuthority ? mintInfo.mintAuthority.toBase58() : 'None'}\n`);
    //   outputStream.write(`Freeze Authority: ${mintInfo.freezeAuthority ? mintInfo.freezeAuthority.toBase58() : 'None'}\n`);
    //   outputStream.write(`Mint is Initialized: ${mintInfo.isInitialized}\n`);
    //   outputStream.write('------------------------\n');
      // Create an object to store token details
      const tokenData = {
        tokenAccount: pubkey.toBase58(),
        mintAddress: mintAddress,
        tokenBalance: tokenBalance,
        decimals: decimals,
        isInitialized: tokenAccount.isInitialized,
        isFrozen: tokenAccount.isFrozen,
        delegate: tokenAccount.delegate ? tokenAccount.delegate.toBase58() : null,
        delegatedAmount: tokenAccount.delegate ? tokenAccount.delegatedAmount.toString() : null,
        closeAuthority: tokenAccount.closeAuthority ? tokenAccount.closeAuthority.toBase58() : null,
        mintInfo: {
          totalSupply: Number(mintInfo.supply) / Math.pow(10, decimals),
          mintAuthority: mintInfo.mintAuthority ? mintInfo.mintAuthority.toBase58() : null,
          freezeAuthority: mintInfo.freezeAuthority ? mintInfo.freezeAuthority.toBase58() : null,
          isMintInitialized: mintInfo.isInitialized,
        },
      };

      // Push the token data to the array
      tokenDataArray.push(tokenData);

      // Wait for 2 seconds before processing the next token
      await delay(500);
    }

    // Save the token data array to the JSON file
    fs.writeFileSync(outputFilePath, JSON.stringify(tokenDataArray, null, 2), 'utf-8'); // 'null, 2' formats the JSON with 2 spaces

  } catch (error) {
    // console.log('');
    // console.error("Error fetching token accounts:", error);
  }
};

printTokens();
