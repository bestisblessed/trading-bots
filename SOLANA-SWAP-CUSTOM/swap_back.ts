import { Transaction, VersionedTransaction, sendAndConfirmTransaction } from '@solana/web3.js';
import { NATIVE_MINT } from '@solana/spl-token';
import axios from 'axios';
import { connection, owner, fetchTokenAccountData, initSdk } from './config';
import { API_URLS } from '@raydium-io/raydium-sdk-v2';

// Get the mint address and percentage of holdings to sell from command-line arguments
const inputMint = process.argv[2];
const percentToSell = parseFloat(process.argv[3]);

// Check if both arguments are provided and valid, else throw an error
if (!inputMint || isNaN(percentToSell) || percentToSell <= 0 || percentToSell > 100) {
  console.error('Error: You must provide a valid mint address and a percentage between 0 and 100.');
  console.error('Usage: ts-node swap_back.ts <mint address> <percentage to sell>');
  process.exit(1);
}

interface SwapCompute {
  id: string
  success: true
  version: 'V0' | 'V1'
  openTime?: undefined
  msg: undefined
  data: {
    swapType: 'BaseIn' | 'BaseOut'
    inputMint: string
    inputAmount: string
    outputMint: string
    outputAmount: string
    otherAmountThreshold: string
    slippageBps: number
    priceImpactPct: number
    routePlan: {
      poolId: string
      inputMint: string
      outputMint: string
      feeMint: string
      feeRate: number
      feeAmount: string
    }[]
  }
}

// Function to calculate the amount to use based on the balance and percentage
const calculateAmountToUse = (balance: number, percent: number): number => {
  return Math.floor(balance * (percent / 100));
};

export const apiSwap = async () => {
  const outputMint = NATIVE_MINT.toBase58(); // SOL

  // Fetch token accounts from the wallet
  const { tokenAccounts } = await fetchTokenAccountData();
  const inputTokenAcc = tokenAccounts.find((a) => a.mint.toBase58() === inputMint);

  if (!inputTokenAcc || !inputTokenAcc.amount) {
    console.error('Token account not found or balance is zero.');
    return;
  }

  // Calculate the amount to sell based on the percentage provided
  const amount = calculateAmountToUse(inputTokenAcc.amount, percentToSell);
  console.log(`\nSwapping ${percentToSell}% of your token holdings (${amount} units)\n`);
  const slippage = 1; // in percent, for this example, 0.5 means 0.5%
  const txVersion: string = 'V0'; // or LEGACY
  const isV0Tx = txVersion === 'V0';
  const [isInputSol, isOutputSol] = [inputMint === NATIVE_MINT.toBase58(), outputMint === NATIVE_MINT.toBase58()];
  const outputTokenAcc = tokenAccounts.find((a) => a.mint.toBase58() === outputMint)?.publicKey;

  if (!inputTokenAcc.publicKey && !isInputSol) {
    console.error('No input token account found.');
    return;
  }

  // Get statistical transaction fee from the API
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
    unwrapSol: isOutputSol, // true means output mint receive SOL, false means output mint received WSOL
    inputAccount: isInputSol ? undefined : inputTokenAcc.publicKey?.toBase58(),
    outputAccount: isOutputSol ? undefined : outputTokenAcc?.toBase58(),
  });

  const allTxBuf = swapTransactions.data.map((tx) => Buffer.from(tx.transaction, 'base64'));
  const allTransactions = allTxBuf.map((txBuf) =>
    isV0Tx ? VersionedTransaction.deserialize(txBuf) : Transaction.from(txBuf)
  );

  console.log(`Total ${allTransactions.length} transactions`, swapTransactions);

  let idx = 0;
  if (!isV0Tx) {
    for (const tx of allTransactions) {
      console.log(`${++idx} transaction sending...`);
      const transaction = tx as Transaction;
      transaction.sign(owner);
      const txId = await sendAndConfirmTransaction(connection, transaction, [owner], { skipPreflight: true });
      console.log(`${++idx} transaction confirmed, txId: ${txId}`);
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
};

// Execute the swap
apiSwap();
