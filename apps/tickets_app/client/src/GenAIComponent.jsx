import React, { useState } from 'react';
import api from './api';

function AIChat() {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    setLoading(true);

    try {
      const res = await api.post('/chat', { prompt: prompt });
      setResponse(res.data.response);
    } catch (error) {
      console.error('Error fetching AI response:', error);
      setResponse('Failed to get response from AI assistant.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-4">
      <h3>Ask AI Assistant</h3>
      <div className="mb-3">
        <textarea
          className="form-control"
          rows="3"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Describe your issue or ask a question..."
        />
      </div>
      <button
        className="btn btn-primary"
        onClick={handleGenerate}
        disabled={loading}
      >
        {loading ? 'Generating...' : 'Submit to AI'}
      </button>

      {response && (
        <div className="card mt-3 p-3 bg-light">
          <h5>AI Answer:</h5>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}

export default AIChat;