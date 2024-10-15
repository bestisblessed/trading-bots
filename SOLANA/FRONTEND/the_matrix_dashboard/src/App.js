import React, { useEffect, useState } from 'react';
import axios from 'axios';
import io from 'socket.io-client';

const socket = io('http://localhost:3000');

function App() {
  const [bots, setBots] = useState([]);

  useEffect(() => {
    axios.get('/api/bots')
      .then(response => setBots(response.data))
      .catch(error => console.error('Error fetching bots:', error));

    socket.on('botUpdate', update => {
      setBots(prevBots => prevBots.map(bot => bot.name === update.name ? update : bot));
    });
  }, []);

  return (
    <div className="App">
      <h1>The Matrix Dashboard</h1>
      <div className="bot-list">
        {bots.map(bot => (
          <div key={bot.name} className="bot">
            <h2>{bot.name}</h2>
            <p>Status: {bot.status}</p>
            <p>Profit: {bot.profit}</p>
            <button onClick={() => controlBot(bot.name, 'start')}>Start</button>
            <button onClick={() => controlBot(bot.name, 'stop')}>Stop</button>
          </div>
        ))}
      </div>
    </div>
  );
}

function controlBot(botName, action) {
  axios.post(`/api/bots/${botName}/${action}`)
    .then(response => console.log(`${action} command sent for ${botName}`))
    .catch(error => console.error('Error controlling bot:', error));
}

export default App;
