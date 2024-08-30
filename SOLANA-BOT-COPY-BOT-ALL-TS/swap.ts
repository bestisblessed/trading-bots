// import { Transaction, VersionedTransaction, sendAndConfirmTransaction } from '@solana/web3.js';
// import { NATIVE_MINT } from '@solana/spl-token';
// import axios from 'axios';
// import { connection, owner, fetchTokenAccountData, initSdk } from './config';
// import { API_URLS } from '@raydium-io/raydium-sdk-v2';
// import fs from 'fs';
// import path from 'path';

// interface SwapCompute {
//   id: string;
//   success: boolean;
//   version: 'V0' | 'V1';
//   data: {
//     swapType: 'BaseIn' | 'BaseOut';
//     inputMint: string;
//     inputAmount: string;
//     outputMint: string;
//     outputAmount: string;
//     otherAmountThreshold: string;
//     slippageBps: number;
//     priceImpactPct: number;
//     routePlan: {
//       poolId: string;
//       inputMint: string;
//       outputMint: string;
//       feeMint: string;
//       feeRate: number;
//       feeAmount: string;
//     }[];
//   };
// }

// // Path to the updated tokens file
// const updatesPath = path.join(__dirname, './data/updated_tokens.json');

// async function processUpdatedTokens() {
//   if (fs.existsSync(updatesPath)) {
//     const updatedTokens = JSON.parse(fs.readFileSync(updatesPath, 'utf-8'));

//     for (const action in updatedTokens) {
//       for (const token of updatedTokens[action]) {
//         const outputMint = token.mint;
//         let solAmount;

//         if (action === 'added') {
//           // Buying 0.005 SOL worth of the added token
//           solAmount = 0.005;
//           console.log(`Buying token with mint: ${outputMint}`);
//         } else if (action === 'removed') {
//           solAmount = await getSellAmount(outputMint);
//           console.log(`Selling token with mint: ${outputMint}`);
//         }

//         if (solAmount) {
//           await performSwap(outputMint, solAmount);
//         }
//       }
//     }

//     fs.unlinkSync(updatesPath);
//     console.log('Processed and removed updated_tokens.json.');
//   } else {
//     console.log('No updated tokens found. Exiting...');
//   }
// }

// async function performSwap(outputMint: string, solAmount: number) {
//   const amount = Math.round(solAmount * 1_000_000_000); // Convert SOL to lamports

//   const inputMint = NATIVE_MINT.toBase58();
//   const slippage = 0.5; // in percent, for this example, 0.5 means 0.5%
//   const txVersion: string = 'V0'; // or LEGACY
//   const isV0Tx = txVersion === 'V0';

//   const [isInputSol, isOutputSol] = [inputMint === NATIVE_MINT.toBase58(), outputMint === NATIVE_MINT.toBase58()];

//   const { tokenAccounts } = await fetchTokenAccountData();
//   const inputTokenAcc = tokenAccounts.find((a) => a.mint.toBase58() === inputMint)?.publicKey;
//   const outputTokenAcc = tokenAccounts.find((a) => a.mint.toBase58() === outputMint)?.publicKey;

//   if (!inputTokenAcc && !isInputSol) {
//     console.error('do not have input token account');
//     return;
//   }

//   const { data } = await axios.get<{
//     id: string;
//     success: boolean;
//     data: { default: { vh: number; h: number; m: number } };
//   }>(`${API_URLS.BASE_HOST}${API_URLS.PRIORITY_FEE}`);

//   const { data: swapResponse } = await axios.get<SwapCompute>(
//     `${API_URLS.SWAP_HOST}/compute/swap-base-in?inputMint=${inputMint}&outputMint=${outputMint}&amount=${amount}&slippageBps=${
//       slippage * 100
//     }&txVersion=${txVersion}`
//   );

//   const { data: swapTransactions } = await axios.post<{
//     id: string;
//     version: string;
//     success: boolean;
//     data: { transaction: string }[];
//   }>(`${API_URLS.SWAP_HOST}/transaction/swap-base-in`, {
//     computeUnitPriceMicroLamports: String(data.data.default.h),
//     swapResponse,
//     txVersion,
//     wallet: owner.publicKey.toBase58(),
//     wrapSol: isInputSol,
//     unwrapSol: isOutputSol, // true means output mint receive sol, false means output mint received wsol
//     inputAccount: isInputSol ? undefined : inputTokenAcc?.toBase58(),
//     outputAccount: isOutputSol ? undefined : outputTokenAcc?.toBase58(),
//   });

//   const allTxBuf = swapTransactions.data.map((tx) => Buffer.from(tx.transaction, 'base64'));
//   const allTransactions = allTxBuf.map((txBuf) =>
//     isV0Tx ? VersionedTransaction.deserialize(txBuf) : Transaction.from(txBuf)
//   );

//   console.log(`total ${allTransactions.length} transactions`, swapTransactions);

//   let idx = 0;
//   if (!isV0Tx) {
//     for (const tx of allTransactions) {
//       console.log(`${++idx} transaction sending...`);
//       const transaction = tx as Transaction;
//       transaction.sign(owner);
//       const txId = await sendAndConfirmTransaction(connection, transaction, [owner], { skipPreflight: true });
//       console.log(`${idx} transaction confirmed, txId: ${txId}`);
//     }
//   } else {
//     for (const tx of allTransactions) {
//       idx++;
//       const transaction = tx as VersionedTransaction;
//       transaction.sign([owner]);
//       const txId = await connection.sendTransaction(tx as VersionedTransaction, { skipPreflight: true });
//       const { lastValidBlockHeight, blockhash } = await connection.getLatestBlockhash({
//         commitment: 'finalized',
//       });
//       console.log(`${idx} transaction sending..., txId: ${txId}`);
//       await connection.confirmTransaction(
//         {
//           blockhash,
//           lastValidBlockHeight,
//           signature: txId,
//         },
//         'confirmed'
//       );
//       console.log(`${idx} transaction confirmed`);
//     }
//   }
// }

// async function getSellAmount(mint: string): Promise<number> {
//   return 0.01; // Placeholder: Calculate and return the amount to sell based on logic
// }

// // Call the main function to process updated tokens
// processUpdatedTokens();
import { Transaction, VersionedTransaction, sendAndConfirmTransaction } from '@solana/web3.js';
import { NATIVE_MINT } from '@solana/spl-token';
import axios from 'axios';
import { connection, owner, fetchTokenAccountData, initSdk } from './config';
import { API_URLS } from '@raydium-io/raydium-sdk-v2';
import fs from 'fs';
import path from 'path';

interface TokenData {
  index: number;
  mint: string;
  owner: string;
  programId: string;
  amount: string;
  decimals: number;
  uiAmountString: string;
}

interface SwapCompute {
  id: string;
  success: boolean;
  version: 'V0' | 'V1';
  data: {
    swapType: 'BaseIn' | 'BaseOut';
    inputMint: string;
    inputAmount: string;
    outputMint: string;
    outputAmount: string;
    otherAmountThreshold: string;
    slippageBps: number;
    priceImpactPct: number;
    routePlan: {
      poolId: string;
      inputMint: string;
      outputMint: string;
      feeMint: string;
      feeRate: number;
      feeAmount: string;
    }[];
  };
}

// Path to the updated tokens file
const updatesPath = path.join(__dirname, './data/updated_tokens.json');
const balancesPath = path.join(__dirname, './data/wallet_token_balances.json'); // Adjust to your balance JSON file path

async function processUpdatedTokens() {
  if (fs.existsSync(updatesPath)) {
    const updatedTokens = JSON.parse(fs.readFileSync(updatesPath, 'utf-8'));

    for (const action in updatedTokens) {
      for (const token of updatedTokens[action]) {
        const outputMint = token.mint;
        let solAmount;

        if (action === 'added') {
          // Buying 0.005 SOL worth of the added token
          solAmount = 0.005;
          console.log(`Buying token with mint: ${outputMint}`);
        } else if (action === 'removed') {
          solAmount = await getSellAmountFromJson(outputMint);
          console.log(`Selling token with mint: ${outputMint}`);
        }

        if (solAmount) {
          await performSwap(outputMint, solAmount);
        }
      }
    }

    fs.unlinkSync(updatesPath);
    console.log('Processed and removed updated_tokens.json.');
  } else {
    console.log('No updated tokens found. Exiting...');
  }
}

// Function to read the balance from the JSON file and calculate 90% of it
async function getSellAmountFromJson(mint: string): Promise<number> {
  if (!fs.existsSync(balancesPath)) {
    console.error(`Balance file not found at ${balancesPath}`);
    return 0;
  }

  const balances: TokenData[] = JSON.parse(fs.readFileSync(balancesPath, 'utf-8'));
  const token = balances.find(t => t.mint === mint);

  if (!token) {
    console.error(`Token with mint ${mint} not found in balance file.`);
    return 0;
  }

  // Convert amount from string to a number
  const tokenBalance = parseFloat(token.uiAmountString);

  // Calculate 90% of the balance
  const sellAmount = tokenBalance * 0.9;

  console.log(`Selling 90% of token with mint: ${mint}, which amounts to ${sellAmount} tokens`);

  // Return the amount to sell in its raw form (unadjusted for decimals)
  return Math.round(sellAmount * (10 ** token.decimals));
}

async function performSwap(outputMint: string, solAmount: number) {
  const amount = Math.round(solAmount * 1_000_000_000); // Convert SOL to lamports

  const inputMint = NATIVE_MINT.toBase58();
  const slippage = 0.5; // in percent, for this example, 0.5 means 0.5%
  const txVersion: string = 'V0'; // or LEGACY
  const isV0Tx = txVersion === 'V0';

  const [isInputSol, isOutputSol] = [inputMint === NATIVE_MINT.toBase58(), outputMint === NATIVE_MINT.toBase58()];

  const { tokenAccounts } = await fetchTokenAccountData();
  const inputTokenAcc = tokenAccounts.find((a) => a.mint.toBase58() === inputMint)?.publicKey;
  const outputTokenAcc = tokenAccounts.find((a) => a.mint.toBase58() === outputMint)?.publicKey;

  if (!inputTokenAcc && !isInputSol) {
    console.error('do not have input token account');
    return;
  }

  const { data } = await axios.get<{
    id: string;
    success: boolean;
    data: { default: { vh: number; h: number; m: number } };
  }>(`${API_URLS.BASE_HOST}${API_URLS.PRIORITY_FEE}`);

  const { data: swapResponse } = await axios.get<SwapCompute>(
    `${API_URLS.SWAP_HOST}/compute/swap-base-in?inputMint=${inputMint}&outputMint=${outputMint}&amount=${amount}&slippageBps=${
      slippage * 100
    }&txVersion=${txVersion}`
  );

  const { data: swapTransactions } = await axios.post<{
    id: string;
    version: string;
    success: boolean;
    data: { transaction: string }[];
  }>(`${API_URLS.SWAP_HOST}/transaction/swap-base-in`, {
    computeUnitPriceMicroLamports: String(data.data.default.h),
    swapResponse,
    txVersion,
    wallet: owner.publicKey.toBase58(),
    wrapSol: isInputSol,
    unwrapSol: isOutputSol, // true means output mint receive sol, false means output mint received wsol
    inputAccount: isInputSol ? undefined : inputTokenAcc?.toBase58(),
    outputAccount: isOutputSol ? undefined : outputTokenAcc?.toBase58(),
  });

  const allTxBuf = swapTransactions.data.map((tx) => Buffer.from(tx.transaction, 'base64'));
  const allTransactions = allTxBuf.map((txBuf) =>
    isV0Tx ? VersionedTransaction.deserialize(txBuf) : Transaction.from(txBuf)
  );

  console.log(`total ${allTransactions.length} transactions`, swapTransactions);

  let idx = 0;
  if (!isV0Tx) {
    for (const tx of allTransactions) {
      console.log(`${++idx} transaction sending...`);
      const transaction = tx as Transaction;
      transaction.sign(owner);
      const txId = await sendAndConfirmTransaction(connection, transaction, [owner], { skipPreflight: true });
      console.log(`${idx} transaction confirmed, txId: ${txId}`);
    }
  } else {
    for (const tx of allTransactions) {
      idx++;
      const transaction = tx as VersionedTransaction;
      transaction.sign([owner]);
      const txId = await connection.sendTransaction(tx as VersionedTransaction, { skipPreflight: true });
      const { lastValidBlockHeight, blockhash } = await connection.getLatestBlockhash({
        commitment: 'finalized',
      });
      console.log(`${idx} transaction sending..., txId: ${txId}`);
      await connection.confirmTransaction(
        {
          blockhash,
          lastValidBlockHeight,
          signature: txId,
        },
        'confirmed'
      );
      console.log(`${idx} transaction confirmed`);
    }
  }
}

// Call the main function to process updated tokens
processUpdatedTokens();