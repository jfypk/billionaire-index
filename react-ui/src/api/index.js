// This file would contain API functions to interact with your backend
// For example:

export const fetchBillionaires = async () => {
  const response = await fetch('/api/billionaires');
  if (!response.ok) {
    throw new Error('Failed to fetch billionaires');
  }
  return response.json();
};

export const submitVote = async (category, weight) => {
  const response = await fetch('/vote', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `category=${category}&weight=${weight}`
  });
  
  if (!response.ok) {
    throw new Error('Vote submission failed');
  }
  
  return response.json();
};
