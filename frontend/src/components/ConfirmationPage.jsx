import React, { useState } from 'react';

function ConfirmationPage({ confirmationCode, moreTasks }) {
  const [copied, setCopied] = useState(false);

  // Function to handle copy to clipboard
  const handleCopyClick = () => {
    // Use the Clipboard API to copy the confirmation code to clipboard
    navigator.clipboard.writeText(confirmationCode)
      .then(() => {
        setCopied(true); // Show success tooltip
        setTimeout(() => setCopied(false), 1000); // Hide success tooltip after 2 seconds
      })
      .catch(err => console.error('Error copying text: ', err));
  };

  return (
    <div className="max-w-lg mx-auto mt-10 p-6 bg-white shadow-lg rounded-md text-center place-items-center">
      <h1 className="text-3xl font-bold mb-4 text-blue-600">Congrats on completing a task!</h1>
      <p className="text-gray-700">Your confirmation code is:</p>
      <div className="w-full max-w-[24.5rem]">
        <div className="relative w-full max-w-[24.5rem]">
          <input 
            id="code-copy-text" 
            type="text" 
            className="col-span-full text-lg font-semibold rounded-lg block w-full px-2.5 py-4" 
            value={confirmationCode} 
            disabled 
            readOnly 
          />
          
          <button 
            onClick={handleCopyClick} 
            className="absolute end-2 top-1/2 -translate-y-1/2 text-gray-500 hover:bg-gray-100 rounded-lg p-2 inline-flex items-center justify-center"
          >
            <span id="default-icon">
              <svg className="w-3.5 h-3.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 18 20">
                <path d="M16 1h-3.278A1.992 1.992 0 0 0 11 0H7a1.993 1.993 0 0 0-1.722 1H2a2 2 0 0 0-2 2v15a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V3a2 2 0 0 0-2-2Zm-3 14H5a1 1 0 0 1 0-2h8a1 1 0 0 1 0 2Zm0-4H5a1 1 0 0 1 0-2h8a1 1 0 1 1 0 2Zm0-5H5a1 1 0 0 1 0-2h2V2h4v2h2a1 1 0 1 1 0 2Z"/>
              </svg>
            </span>
            <span id="success-icon" className={`hidden inline-flex items-center ${copied ? 'inline-flex' : 'hidden'}`}>
              <svg className="w-3.5 h-3.5 text-blue-700 dark:text-blue-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 16 12">
                <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M1 5.917 5.724 10.5 15 1.5"/>
              </svg>
            </span>
          </button>
          
          <div id="tooltip-copy-code-copy-text" role="tooltip" className={`absolute z-10 inline-block px-3 py-2 text-sm font-medium text-white transition-opacity duration-300 bg-gray-900 rounded-lg shadow-sm opacity-0 tooltip dark:bg-gray-700 ${copied ? 'opacity-100' : 'invisible'}`}>
            <span id="default-tooltip-message">{copied ? 'Copied!' : 'Copy to clipboard'}</span>
            <div className="tooltip-arrow" data-popper-arrow></div>
          </div>
        </div>
      </div>

      <p className="text-gray-700 mb-6">Please copy this code. Afterwards, return to the MTurk HIT and input the code to claim your payment.</p>
      
      <div className="flex justify-center space-x-4">
        <button
          onClick={moreTasks}
          className="px-6 py-3 bg-blue-950 text-white font-semibold rounded-md hover:bg-blue-700 transition duration-200"
        >
          Complete Another Task
        </button>
      </div>
    </div>
  );
}

export default ConfirmationPage;