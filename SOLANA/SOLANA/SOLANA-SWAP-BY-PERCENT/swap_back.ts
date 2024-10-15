import { Transaction, VersionedTransaction, sendAndConfirmTransaction } from '@solana/web3.js';
import { NATIVE_MINT } from '@solana/spl-token';
import axios from 'axios';
import { connection, owner, fetchTokenAccountData, initSdk } from './config';
import { API_URLS } from '@raydium-io/raydium-sdk-v2';

interface SwapCompute {
  id: string;
  success: true;
  version: 'V0' | 'V1';
  openTime?: undefined;
  msg: undefined;
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

// Function to calculate 95% of the NILLY balance
const calculateAmountToUse = (balance: number): number => {
  return Math.floor(balance * 0.5); // Calculate 95% of the balance
};

export const apiSwap = async () => {
  const inputMint = '9RxQeMi2MRjiFU2ZfPWirP8M242KMhoyW9SB1UvfVXhu'; // NILLY
  const outputMint = NATIVE_MINT.toBase58(); // SOL

  // Fetch token accounts from the wallet
  const { tokenAccounts } = await fetchTokenAccountData();
  const inputTokenAcc = tokenAccounts.find((a) => a.mint.toBase58() === inputMint);

  if (!inputTokenAcc || !inputTokenAcc.amount) {
    console.error('NILLY token account not found or balance is zero.');
    return;
  }

  // Calculate 95% of the NILLY balance
  const amount = calculateAmountToUse(inputTokenAcc.amount);

  // Print the amount to swap
  console.log(`\nSwapping 95% of NILLY Balance: ${amount} NILLY\n`);

  const slippage = 0.5; // in percent, for this example, 0.5 means 0.5%
  const txVersion: string = 'V0'; // or LEGACY
  const isV0Tx = txVersion === 'V0';

  const [isInputSol, isOutputSol] = [inputMint === NATIVE_MINT.toBase58(), outputMint === NATIVE_MINT.toBase58()];

  const outputTokenAcc = tokenAccounts.find((a) => a.mint.toBase58() === outputMint)?.publicKey;

  // Adjusted the following check to ensure inputTokenAcc.publicKey is defined
  if (!inputTokenAcc.publicKey && !isInputSol) {
    console.error('No input token account found.');
    return;
  }

  // get statistical transaction fee from api
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

  console.log(`total ${allTransactions.length} transactions`, swapTransactions);

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
