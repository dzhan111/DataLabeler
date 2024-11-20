import React, { useState } from 'react';

function InputPage({ onSubmit }) {
  const [id, setId] = useState('');

  const handleSubmit = () => {
    if (id.trim()) {
      onSubmit(id);
    } 
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-4xl font-bold text-center mb-6 text-gray-800">Welcome to DataLabeler. </h1>
      <h2 className="text-xl font-bold text-center mb-6 text-gray-500 max-w-md">We turn your words into money. Enter your MTurk ID to begin.</h2>
      <div className="w-full max-w-md bg-white shadow-md rounded-lg p-8">
        <h1 className="text-2xl font-bold text-center mb-6 text-gray-800">
          Enter MTurk ID
        </h1>
        <div className="space-y-4">
          <input 
            value={id} 
            onChange={(e) => setId(e.target.value)} 
            placeholder="MTurk ID" 
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button 
            onClick={handleSubmit} 
            disabled={!id.trim()}
            className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition-colors duration-300 disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}

export default InputPage;