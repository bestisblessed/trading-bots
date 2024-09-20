import { Connection, PublicKey } from '@solana/web3.js';
import { TOKEN_PROGRAM_ID, getAccount, getMint } from '@solana/spl-token';
import { connection, owner } from './config'; // Assumes your connection and owner are set up in config.ts

// Helper function to create a delay (2 seconds in this case)
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

const printTokens = async () => {
  try {
    // Fetch all token accounts owned by the wallet
    const tokenAccounts = await connection.getTokenAccountsByOwner(
      owner.publicKey,
      { programId: TOKEN_PROGRAM_ID }
    );

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

      // Mint details
      console.log(`Total Supply: ${Number(mintInfo.supply) / Math.pow(10, decimals)}`);
      console.log(`Mint Authority: ${mintInfo.mintAuthority ? mintInfo.mintAuthority.toBase58() : 'None'}`);
      console.log(`Freeze Authority: ${mintInfo.freezeAuthority ? mintInfo.freezeAuthority.toBase58() : 'None'}`);
      console.log(`Mint is Initialized: ${mintInfo.isInitialized}`);
      console.log('------------------------');

      // Wait for 2 seconds before processing the next token
      await delay(500);
    }
  } catch (error) {
    // console.log('');
    // console.error("Error fetching token accounts:", error);
  }
};

printTokens();
