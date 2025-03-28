import { useState } from 'react';
import './App.css';
import botLogo from './assets/botlogo.png'; // Import the logo here

function App() {
  const [input, setInput] = useState('');
  const [conversation, setConversation] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { role: 'user', text: input };
    setConversation(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const response = await fetch('https://q1vaiw9s90.execute-api.us-east-1.amazonaws.com/prod/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      });

      const data = await response.json();
      const botMsg = { role: 'bot', text: data.response || '[No response]' };
      setConversation(prev => [...prev, botMsg]);
    } catch (error) {
      setConversation(prev => [...prev, { role: 'bot', text: '[Error contacting chatbot]' }]);
    }

    setInput('');
    setLoading(false);
  };

  return (
    <div className="app">
      {/* Add the logo */}
      <div className="logo">
        <img src={botLogo} alt="Healthcare Assistant Logo" style={{ width: '100px', marginBottom: '20px' }} />
      </div>

      <h2>💬 Virtual Healthcare Assistant</h2>
      <div className="chat-window">
        {conversation.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <strong>{msg.role === 'user' ? 'You' : 'Bot'}:</strong> {msg.text}
          </div>
        ))}
        {loading && <div className="message bot"><strong>Bot:</strong> Typing...</div>}
      </div>
      <div className="input-area">
        <input
          type="text"
          placeholder="Ask something..."
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;
