import React, { useState } from "react";
import InputForm from "./InputForm"; // Import InputForm for file upload functionality

import { useTheme } from "@material-tailwind/react";

import axios from "axios";

const Chatbot = () => {
  // Chatbot component for user interaction

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    // Function to send user messages

    setMessages([...messages, { sender: "user", text: input }]);

    const res = await axios.post("http://localhost:5000/api/chat", {
      input: input, // Changed key to match the API
    });
    setMessages([
      ...messages,
      { sender: "user", text: input },
      { sender: "bot", text: res.data.response },
    ]);
    setInput("");
  };

  const theme = useTheme();

  return (
    // Render the chatbot interface

    <div
      className="chat-container"
      style={{ backgroundColor: theme.colors.background }}
    >
      <div className="chat-box" style={{ color: theme.colors.text }}>
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <input // Input field for user messages
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        style={{
          backgroundColor: theme.colors.secondary,
          color: theme.colors.text,
        }}
      />
      <button // Button to send the message
        onClick={sendMessage}
        style={{
          backgroundColor: theme.colors.primary,
          color: theme.colors.secondary,
        }}
      >
        Send
      </button>
    </div> // End of chat container
  );
};

export default Chatbot;
