// const web3 = require("@solana/web3.js");
// (async () => {
//   const solana = new web3.Connection("https://tiniest-burned-mansion.solana-mainnet.quiknode.pro/a5f42fa1b144c8f334deb792e7567894965b96b0/");
//   console.log(await solana.getSlot());
// })();
const WebSocket = require('ws');
const ws = new WebSocket('wss://tiniest-burned-mansion.solana-mainnet.quiknode.pro/ws/a5f42fa1b144c8f334deb792e7567894965b96b0/');

ws.on('open', function open() {
  console.log('WebSocket connection opened.');
});

ws.on('message', function message(data) {
  console.log('Received data:', data);
});

ws.on('error', function error(err) {
  console.error('WebSocket error:', err);
});

ws.on('close', function close() {
  console.log('WebSocket connection closed.');
});
