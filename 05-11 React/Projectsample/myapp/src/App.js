// in src/App.js
import React, { useEffect, useState } from 'react';

function App() {
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        fetch('http://localhost:8000/api/messages/')
            .then(response => response.json())
            .then(data => setMessages(data));
    }, []);

    return (
        <div className="App">
            {messages.map(message => (
                <p key={message.id}>{message.content}</p>
            ))}
        </div>
    );
}

export default App;
