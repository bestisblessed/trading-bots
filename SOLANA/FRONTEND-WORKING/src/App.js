import React, { useState, useEffect } from 'react';
import { getBalance, triggerSwap } from './api';  // Define API requests

function App() {
  const [walletBalance, setWalletBalance] = useState([]);
  const [token, setToken] = useState('');
  const [amount, setAmount] = useState('');

  // Fetch wallet balance
  useEffect(() => {
    const fetchBalance = async () => {
      const balance = await getBalance();
      setWalletBalance(balance);
    };
    fetchBalance();
  }, []);

  // Handle swap form submission
  const handleSwap = async (e) => {
    e.preventDefault();
    await triggerSwap(token, amount);
    alert('Swap triggered');
  };

  return (
    <div className="App">
      <h1>Solana Trading Bot</h1>

      <div className="wallet-balance">
        <h2>Wallet Balances</h2>
        <ul>
          {walletBalance.map((item, index) => (
            <li key={index}>{item.token}: {item.amount}</li>
          ))}
        </ul>
      </div>

      <div className="swap">
        <h2>Manual Swap</h2>
        <form onSubmit={handleSwap}>
          <input 
            type="text" 
            placeholder="Token" 
            value={token} 
            onChange={(e) => setToken(e.target.value)} 
          />
          <input 
            type="number" 
            placeholder="Amount" 
            value={amount} 
            onChange={(e) => setAmount(e.target.value)} 
          />
          <button type="submit">Swap</button>
        </form>
      </div>
    </div>
  );
}

export default App;
