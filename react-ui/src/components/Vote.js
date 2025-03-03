import React, { useState } from 'react';

function Vote() {
  const [weights, setWeights] = useState({
    social: 30,
    environmental: 20,
    political: 20,
    philanthropy: 20,
    cultural: 10
  });
  const [message, setMessage] = useState({ text: '', type: '' });
  const [showMessage, setShowMessage] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setWeights(prev => ({
      ...prev,
      [name]: parseInt(value, 10)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const total = Object.values(weights).reduce((sum, val) => sum + val, 0);
    const normalizedWeights = {};
    
    for (const [category, weight] of Object.entries(weights)) {
      normalizedWeights[category] = weight / total;
    }
    
    try {
      for (const [category, weight] of Object.entries(normalizedWeights)) {
        const response = await fetch('/vote', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: `category=${category}&weight=${weight}`
        });
        
        if (!response.ok) throw new Error('Vote failed');
      }
      
      setMessage({ text: 'Votes submitted successfully!', type: 'success' });
      setShowMessage(true);
    } catch (error) {
      console.error('Error submitting vote:', error);
      setMessage({ text: 'Error submitting vote. Please try again.', type: 'error' });
      setShowMessage(true);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">Vote on Category Weights</h1>
      
      <div className="bg-white shadow-lg rounded-lg p-6">
        <p className="mb-4 text-gray-600">
          Adjust the importance of each category in the overall impact score. 
          The weights will be normalized to sum to 100%.
        </p>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Social Impact (Worker treatment, tax practices)</label>
              <input 
                type="range" 
                name="social" 
                min="0" 
                max="100" 
                value={weights.social} 
                onChange={handleChange}
                className="mt-1 w-full" 
              />
              <output className="text-sm text-gray-500">{weights.social}%</output>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Environmental Responsibility</label>
              <input 
                type="range" 
                name="environmental" 
                min="0" 
                max="100" 
                value={weights.environmental}
                onChange={handleChange}
                className="mt-1 w-full" 
              />
              <output className="text-sm text-gray-500">{weights.environmental}%</output>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Political Influence</label>
              <input 
                type="range" 
                name="political" 
                min="0" 
                max="100" 
                value={weights.political}
                onChange={handleChange}
                className="mt-1 w-full" 
              />
              <output className="text-sm text-gray-500">{weights.political}%</output>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Philanthropy</label>
              <input 
                type="range" 
                name="philanthropy" 
                min="0" 
                max="100" 
                value={weights.philanthropy}
                onChange={handleChange}
                className="mt-1 w-full" 
              />
              <output className="text-sm text-gray-500">{weights.philanthropy}%</output>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Cultural Impact</label>
              <input 
                type="range" 
                name="cultural" 
                min="0" 
                max="100" 
                value={weights.cultural}
                onChange={handleChange}
                className="mt-1 w-full" 
              />
              <output className="text-sm text-gray-500">{weights.cultural}%</output>
            </div>
          </div>

          <div className="flex justify-end">
            <button type="submit" className="py-2 px-4 bg-blue-500 hover:bg-blue-600 text-white rounded-lg">
              Submit Vote
            </button>
          </div>
        </form>

        {showMessage && (
          <div className={`mt-4 p-4 rounded-lg ${message.type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
            {message.text}
          </div>
        )}
      </div>
    </div>
  );
}

export default Vote;
