# Detecting new tokens

To detect tokens created in ways that are not captured by the txlistinternal endpoint, you can consider the following strategies:

1. Monitoring txlist Endpoint for Specific Events
Track Token Creation in Regular Transactions: Tokens might be created as part of standard user transactions rather than internal transactions. By monitoring the txlist endpoint, which lists all normal transactions for a given address, you can identify transactions that include contract creation, even if they aren't internal transactions.
Check for contractAddress Field: The txlist endpoint will sometimes include a contractAddress field in the transaction result if the transaction resulted in the creation of a new contract. You can use this to identify when a new token contract is deployed.
2. Event Logs (getLogs Endpoint)
Monitor for Transfer Events: Use the getLogs endpoint to monitor for Transfer events, which are part of the ERC-20 standard and are emitted whenever tokens are transferred. By monitoring logs across all blocks, you can detect tokens being transferred for the first time, which could indicate the creation of new tokens.
Look for Specific Events: Beyond Transfer events, some tokens emit specific events upon creation or during initial distribution (e.g., Mint events). You can search for these events specifically.
3. Monitor Known DEXes and DeFi Protocols
DEX Trades: New tokens often appear on decentralized exchanges (DEXes) shortly after being created. By monitoring DEX activity (using endpoints from DEXs like Uniswap or services like Dexscreener), you can detect new tokens as soon as they are listed or traded.
Liquidity Pool Creations: Many tokens are first added to liquidity pools on DEXes. Monitoring the creation of new liquidity pools can help you detect new tokens.
4. On-Chain Indexing Services
Use Third-Party Indexing Services: Services like The Graph or Bitquery can be used to query specific events across the blockchain. These services often index more than just transaction data and can include a broader range of on-chain activities, making it easier to detect new tokens.
Create a Custom Indexer: If you need more granular control, you could build a custom indexer that monitors the blockchain for specific events, including both standard and internal transactions, as well as logs and other data.
5. Cross-Referencing with Token Listings
Automated Token Listings: Monitor platforms that list new tokens (like CoinGecko, CoinMarketCap, or DEX tools) to cross-reference tokens you detect on-chain with those listed publicly. This can help ensure you're aware of all new tokens, regardless of how they were created.
Implementation Tips:
Combine Multiple Endpoints: You might need to use a combination of txlist, txlistinternal, and getLogs endpoints to fully capture all potential token creation events.
Regular Polling or Webhooks: Consider setting up regular polling or subscribing to webhooks (if available) to get real-time notifications of new token creations.

# Method ID and Function Call Analysis
Function Calls:
Function calls in smart contracts are the core operations that users or bots execute on the blockchain. By analyzing these function calls, you can gain insights into what actions are being taken on specific contracts (e.g., swapping tokens, adding liquidity, etc.). Understanding the nature of these function calls can help tailor your bot’s strategy to capitalize on specific patterns or avoid risky situations.

Identifying Function Calls:

Common Function Calls: Some common function calls you might encounter include:
swapExactETHForTokens: Swapping ETH for a specified amount of tokens.
swapTokensForExactETH: Swapping a specified amount of tokens for ETH.
addLiquidity: Adding liquidity to a liquidity pool, receiving LP (Liquidity Provider) tokens in return.
removeLiquidity: Removing liquidity from a pool, which returns the underlying assets to the user.
Transaction Input Data: Each function call is encoded in the transaction’s input data. The first four bytes of this data are known as the Method ID, which uniquely identifies the function being called. By decoding the input data, your bot can identify what action is being taken and respond accordingly.
Practical Implementation in Trading Bots:

Trade Execution: By analyzing function calls like swapExactETHForTokens, your bot can determine when large swaps are happening and either follow the trend or counteract it (e.g., avoiding slippage by front-running or trailing).
Liquidity Monitoring: Monitoring addLiquidity and removeLiquidity function calls can help your bot understand shifts in liquidity. For example, a sudden increase in liquidity might stabilize a token’s price, while a sudden decrease might cause volatility, prompting your bot to act accordingly.
Event-Driven Strategies: Your bot can react to specific function calls by adjusting its strategy dynamically. For example, if it detects a high frequency of removeLiquidity calls, it might anticipate a price drop and sell tokens before the price crashes.

# cont (MethodId and functionName)
Common methodId and functionName Mappings on Base Blockchain:
0x095ea7b3 - approve(address spender, uint256 amount)

This method is used to approve a specified amount of tokens for a particular spender, allowing them to transfer the tokens on behalf of the user.
0x18cbafe5 - swapExactTokensForETH(uint256 amountIn, uint256 amountOutMin, address[] path, address to, uint256 deadline)

This method is often associated with DEX operations where a user swaps a specific amount of tokens for ETH.
0x23b872dd - transferFrom(address from, address to, uint256 value)

This method allows a user to transfer tokens on behalf of another address, usually after the approve function has been called.
0x7ff36ab5 - swapExactETHForTokens(uint256 amountOutMin, address[] path, address to, uint256 deadline)

Commonly used for swapping ETH for tokens on DEXes like Uniswap.
0xa9059cbb - transfer(address to, uint256 value)

This is a simple transfer method, used to send tokens from one address to another.
0x3593564c - execute(bytes commands, bytes[] inputs, uint256 deadline)

This method is part of a more complex contract operation, often involving multi-step transactions in protocols.
Analyzing and Utilizing These IDs:
Method ID Analysis:

Differentiating Transactions: By decoding the method ID, you can identify whether a transaction is a simple token transfer, a DEX trade, a liquidity provision, or another type of contract interaction.
Strategic Decisions: Knowing the specific functions being called can help your trading bot make informed decisions. For instance, detecting swapExactETHForTokens might trigger your bot to monitor price impacts on a DEX.
Identifying Patterns and Bots:

Bot Detection: Repeated patterns of certain method IDs in quick succession might indicate bot activity, such as front-running or sandwich attacks. Understanding these patterns can help your bot either mimic successful strategies or avoid unfavorable transactions.
Understanding Complex Transactions:

Function Call Analysis: The execute function and similar methods often involve multi-step operations that could represent more sophisticated financial maneuvers. Analyzing these can provide deeper insights into market movements.
By analyzing these methodId and functionName mappings, your bot can better understand the nature of transactions on the Base blockchain and react accordingly. This can be critical for optimizing trading strategies, detecting potential threats, and making data-driven decisions.




# TRANSACTIONS 
Difference Between Normal and Internal Transactions
1. Normal Transactions:
- What Are They?
  - Normal transactions are the most common type of transactions on a blockchain like Ethereum or Base. They represent the transfer of Ether (or other tokens) from one externally owned account (EOA) to another.
  - A normal transaction is initiated and signed by a user’s private key, and it directly modifies the blockchain’s state by transferring Ether or calling a smart contract.

- Example:
  - When you send Ether from your MetaMask wallet to another wallet, that’s a normal transaction.

- Characteristics:
  - Triggered by: Externally owned accounts (EOAs) using private keys.
  - Direct interaction: Can directly call a smart contract function or transfer funds.
  - Visibility: Recorded directly on the blockchain as a transaction with a unique transaction hash.

2. Internal Transactions:
- What Are They?
  - Internal transactions, also known as "message calls" or "sub-calls," occur within the context of a smart contract. They are not transactions initiated by an EOA, but rather transactions triggered by the execution of a smart contract.
  - These are often the result of contract-to-contract interactions, where one smart contract calls another smart contract or transfers Ether as part of its logic.

- Example:
  - If you call a smart contract that, as part of its function, sends Ether to another address, that Ether transfer is an internal transaction.
  - For instance, in a decentralized exchange (DEX), when you swap tokens, the contract might internally send some Ether to another contract or address as part of the swap process.

- Characteristics:
  - Triggered by: Smart contracts during their execution, not by EOAs directly.
  - Indirect interaction: Part of the execution of a smart contract's logic.
  - Visibility: Not recorded as a standard transaction with its own hash; instead, they are logged as part of the execution trace of the smart contract.

Why Internal Transactions Matter:
- Complexity: Internal transactions are crucial for understanding the full scope of smart contract operations, as they often include critical parts of the logic such as transferring funds, interacting with other contracts, or managing internal states.
- Visibility: They are not always visible in the standard transaction list on block explorers, so additional tools or API endpoints (like the one provided by BaseScan) are required to view them.

In Summary:
- Normal Transactions are direct transactions between EOAs or between an EOA and a smart contract. They are easily tracked and visible on the blockchain with a unique transaction hash.
- Internal Transactions occur within the execution of smart contracts and do not have their own transaction hash. They are part of the broader operation of smart contracts and are crucial for understanding contract interactions and fund flows within the contract








ADDRESSES:

Uniswap:
Uniswap V2:
Router: 0x7a250d5630b4cf539739df2c5dacf5c8a1b7026e

This is the primary address to check for most transactions involving Uniswap V2. Users interact with this router for swaps, adding/removing liquidity, etc.
Factory: 0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f

The factory contract is responsible for creating new pairs (liquidity pools). While it's important, most user-facing transactions don't interact directly with the factory.
Pair Contracts: These are specific to each trading pair (e.g., ETH/DAI, USDC/ETH). Each pair has its own contract address, but tracking all pair contracts is complex and usually unnecessary for categorizing buy/sell transactions.

Uniswap V3:
Router: 0xe592427a0aece92de3edee1f18e0157c05861564
This is the primary router address for Uniswap V3, used for all swapping activities.
Factory: 0x1F98431c8aD98523631AE4a59f267346ea31F984
Similar to V2, the factory contract for V3 handles the creation of pools but is not typically interacted with directly by users in swaps.

For checking transactions on the Base chain, the specific DEX router addresses you need to look for include the following:
Uniswap V3 SwapRouter02 - 0x2626664c2603336E57B271c5C0b26F421741e481
BaseSwap Router - 0x16e71b13fE6079B4312063F7E81F76d165Ad32Ad


Sushiswap:
Sushiswap Router: 0xd9e1ce17f2641f24aede4e5b4fce31d6e7f1f8c6
Sushiswap uses this address for routing trades.


PancakeSwap (if you are working with Binance Smart Chain):
PancakeSwap V2 Router: 0x10ed43c718714eb63d5aa57b78b54704e256024e


BaseSwap:
BaseSwap Router: 0x16e71b13fE6079B4312063F7E81F76d165Ad32Ad