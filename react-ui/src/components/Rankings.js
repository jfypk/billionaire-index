import React, { useState, useEffect } from 'react';

function Rankings() {
  const [billionaires, setBillionaires] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBillionaires = async () => {
      try {
        const response = await fetch('/api/billionaires');
        if (!response.ok) {
          throw new Error('Failed to fetch billionaires data');
        }
        const data = await response.json();
        setBillionaires(data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchBillionaires();
  }, []);

  if (loading) return <div className="text-center py-10">Loading...</div>;
  if (error) return <div className="text-center py-10 text-red-500">Error: {error}</div>;

  return (
    <div className="container mx-auto px-4">
      <h1 className="text-3xl font-bold mb-8">Impact Rankings</h1>

      <div className="bg-white shadow-lg rounded-lg overflow-x-auto">
        <table className="w-full table-fixed">
          <thead className="bg-gray-50">
            <tr>
              <th className="w-20 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">Rank</th>
              <th className="w-64 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">Name</th>
              <th className="w-36 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">
                <div className="group relative inline-block">
                  Net Worth
                  <div className="opacity-0 group-hover:opacity-100 transition duration-300 bg-black text-white text-xs rounded-lg py-2 px-3 absolute z-10 top-full left-1/2 transform -translate-x-1/2 mt-2 min-w-[200px]">
                    Net worth in billions of USD
                  </div>
                </div>
              </th>
              <th className="w-36 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">
                <div className="group relative inline-block">
                  Overall Score
                  <div className="opacity-0 group-hover:opacity-100 transition duration-300 bg-black text-white text-xs rounded-lg py-2 px-3 absolute z-10 top-full left-1/2 transform -translate-x-1/2 mt-2 min-w-[200px]">
                    Weighted average of all impact categories. Score above 15 indicates exceptional positive impact, 8-15 moderate impact, below 8 needs improvement.
                  </div>
                </div>
              </th>
              <th className="w-32 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">
                <div className="group relative inline-block">
                  Social
                  <div className="opacity-0 group-hover:opacity-100 transition duration-300 bg-black text-white text-xs rounded-lg py-2 px-3 absolute z-10 top-full left-1/2 transform -translate-x-1/2 mt-2 min-w-[200px]">
                    Measures worker treatment, tax practices, and corporate governance. High scores (20-30) indicate fair labor practices and ethical business conduct.
                  </div>
                </div>
              </th>
              <th className="w-32 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">
                <div className="group relative inline-block">
                  Environmental
                  <div className="opacity-0 group-hover:opacity-100 transition duration-300 bg-black text-white text-xs rounded-lg py-2 px-3 absolute z-10 top-full left-1/2 transform -translate-x-1/2 mt-2 min-w-[200px]">
                    Based on climate action and sustainability initiatives. High scores (15-20) show strong environmental leadership and innovation.
                  </div>
                </div>
              </th>
              <th className="w-32 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">
                <div className="group relative inline-block">
                  Political
                  <div className="opacity-0 group-hover:opacity-100 transition duration-300 bg-black text-white text-xs rounded-lg py-2 px-3 absolute z-10 top-full left-1/2 transform -translate-x-1/2 mt-2 min-w-[200px]">
                    Evaluates lobbying transparency and campaign contributions. High scores (15-20) indicate ethical political engagement.
                  </div>
                </div>
              </th>
              <th className="w-32 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">
                <div className="group relative inline-block">
                  Philanthropy
                  <div className="opacity-0 group-hover:opacity-100 transition duration-300 bg-black text-white text-xs rounded-lg py-2 px-3 absolute z-10 top-full left-1/2 transform -translate-x-1/2 mt-2 min-w-[200px]">
                    Assesses charitable giving and social impact. High scores (15-20) reflect meaningful contributions to public good.
                  </div>
                </div>
              </th>
              <th className="w-32 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">
                <div className="group relative inline-block">
                  Cultural
                  <div className="opacity-0 group-hover:opacity-100 transition duration-300 bg-black text-white text-xs rounded-lg py-2 px-3 absolute z-10 top-full left-1/2 transform -translate-x-1/2 mt-2 min-w-[200px]">
                    Measures public influence and media representation. High scores (8-10) indicate positive cultural impact.
                  </div>
                </div>
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {billionaires.map((billionaire, index) => (
              <tr key={billionaire.id || index}>
                <td className="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{index + 1}</td>
                <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-500">{billionaire.name}</td>
                <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-500">${billionaire.net_worth.toFixed(2)}B</td>
                <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-500">{billionaire.overall_score.toFixed(1)}</td>
                <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-500">{billionaire.social_score.toFixed(1)}</td>
                <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-500">{billionaire.environmental_score.toFixed(1)}</td>
                <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-500">{billionaire.political_score.toFixed(1)}</td>
                <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-500">{billionaire.philanthropy_score.toFixed(1)}</td>
                <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-500">{billionaire.cultural_score.toFixed(1)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Rankings;
