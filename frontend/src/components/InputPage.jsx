import React, { useState } from 'react';

function InputPage({ onSubmit }) {
  const [id, setId] = useState('');

  const handleSubmit = () => {
    if (id.trim()) {
      onSubmit(id);
    }
  };

  return (
    <div>
      <h1>Enter MTurk ID</h1>
      <input value={id} onChange={(e) => setId(e.target.value)} placeholder="MTurk ID" />
      <button onClick={handleSubmit}>Next</button>
    </div>
  );
}

export default InputPage;