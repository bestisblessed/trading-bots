// Guide for Raydium Trade API
// You can follow the demo implementation in sdk v2 demo.

// Installation

// Copy
// $ yarn add @raydium-io/raydium-sdk-v2
// Import libraries

// Copy
// import { Transaction, VersionedTransaction, sendAndConfirmTransaction } from '@solana/web3.js'
// import { NATIVE_MINT } from '@solana/spl-token'
// import axios from 'axios'
// import { connection, owner, fetchTokenAccountData } from '../config'
// import { API_URLS } from '@raydium-io/raydium-sdk-v2'
// Set up your RPC connection and wallet in a config.ts file following this template.

// You can paste in a burner private key for testing purposes but it's not recommended for production.

// Copy
// export const owner: Keypair = Keypair.fromSecretKey(bs58.decode('<YOUR_WALLET_SECRET_KEY>'))
// export const connection = new Connection('<YOUR_RPC_URL>') //<YOUR_RPC_URL>
// Get quote (https://api-v3.raydium.io/compute/$) & and define the swap type.

// Copy
// const { data: swapResponse } = await axios.get<SwapCompute>(
//     `${
//       API_URLS.SWAP_HOST
//     }/compute/swap-base-in?inputMint=${inputMint}&outputMint=${outputMint}&amount=${amount}&slippageBps=${
//       slippage * 100}&txVersion=${txVersion}`
//   ) // Use the URL xxx/swap-base-in or xxx/swap-base-out to define the swap type. 
 
// 'BaseOut' swaps will get you a quote for the ExactOut amount of token received. 
// In this mode, slippage is inputted to the base token.

// Serialize (https://api-v3.raydium.io/transaction/$)

// Copy
//  const { data: swapTransactions } = await axios.post<{
//     id: string
//     version: string
//     success: boolean
//     data: { transaction: string }[]
//   }>(`${API_URLS.SWAP_HOST}/transaction/swap-base-in`, {
//     computeUnitPriceMicroLamports: String(data.data.default.h),
//     swapResponse,
//     txVersion,
//     wallet: owner.publicKey.toBase58(),
//     wrapSol: isInputSol,
//     unwrapSol: isOutputSol, // true means output mint receive sol, false means output mint received wsol
//     inputAccount: isInputSol ? undefined : inputTokenAcc?.toBase58(),
//     outputAccount: isOutputSol ? undefined : outputTokenAcc?.toBase58(),
//   })
// Deserialize 

// Copy
//   const allTxBuf = swapTransactions.data.map((tx) => Buffer.from(tx.transaction, 'base64'))
//   const allTransactions = allTxBuf.map((txBuf) =>
//     isV0Tx ? VersionedTransaction.deserialize(txBuf) : Transaction.from(txBuf)
//   )

//   console.log(`total ${allTransactions.length} transactions`, swapTransactions)
// Sign and execute

// Copy
//   let idx = 0
//   if (!isV0Tx) {
//     for (const tx of allTransactions) {
//       console.log(`${++idx} transaction sending...`)
//       const transaction = tx as Transaction
//       transaction.sign(owner)
//       const txId = await sendAndConfirmTransaction(connection, transaction, [owner], { skipPreflight: true })
//       console.log(`${++idx} transaction confirmed, txId: ${txId}`)
//     }
//   } else {
//     for (const tx of allTransactions) {
//       idx++
//       const transaction = tx as VersionedTransaction
//       transaction.sign([owner])
//       const txId = await connection.sendTransaction(tx as VersionedTransaction, { skipPreflight: true })
//       const { lastValidBlockHeight, blockhash } = await connection.getLatestBlockhash({
//         commitment: 'finalized',
//       })
//       console.log(`${idx} transaction sending..., txId: ${txId}`)
//       await connection.confirmTransaction(
//         {
//           blockhash,
//           lastValidBlockHeight,
//           signature: txId,
//         },
//         'confirmed'
//       )
//       console.log(`${idx} transaction confirmed`)
// Setting priority fee
// You'll need to get historical data if you'd like to optimize your priority using Raydium API.

// Copy
//   // get statistical transaction fee from API
//   /**
//    * vh: very high
//    * h: high
//    * m: medium
//    */
//   const { data } = await axios.get<{
//     id: string
//     success: boolean
//     data: { default: { vh: number; h: number; m: number } }
//   }>(`${API_URLS.BASE_HOST}${API_URLS.PRIORITY_FEE}`)
// Then, set computeUnitPriceMicroLamports to one of the default tier.

// Copy
//  }>(`${API_URLS.SWAP_HOST}/transaction/swap-base-in`, {
//     computeUnitPriceMicroLamports: String(data.data.default.h) // or custom lamport number.
// If you are looking for a more integrated solution check Raydium SDK here:https://github.com/raydium-io/raydium-sdk-V2/tree/master