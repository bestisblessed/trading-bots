export const getBalance = async () => {
  const response = await fetch('/api/balance');
  const data = await response.json();
  return data;
};

export const triggerSwap = async (token, amount) => {
  const response = await fetch('/api/swap', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ token, amount })
  });
  return await response.json();
};
