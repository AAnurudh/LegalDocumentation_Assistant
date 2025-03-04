import React, { useState } from "react";
import { motion } from "framer-motion";

const LegalAssistant = () => {
  const [file, setFile] = useState(null);
  const [chatInput, setChatInput] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  const handleChatSubmit = async () => {
    if (!chatInput) {
      alert("Please enter a query.");
      return;
    }

    const queryResponse = await fetch("http://localhost:5000/api/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: chatInput }),
    });

    if (queryResponse.ok) {
      const data = await queryResponse.json();
      setChatHistory([...chatHistory, { user: chatInput, bot: data.response }]);
    } else {
      alert("Failed to get response from the bot.");
    }
    setChatInput("");
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("document", file);

    try {
      const response = await fetch("http://localhost:5000/api/upload", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        alert("File uploaded successfully!");
      } else {
        alert("File upload failed.");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("An error occurred while uploading the file.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-r from-blue-500 to-green-500 p-6">
      <motion.h1
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-4xl font-extrabold text-white mb-6 tracking-wide animate-pulse"
      >
        LEGAL ASSISTANT
      </motion.h1>
      <div className="w-full max-w-2xl bg-white p-6 rounded-lg shadow-xl border border-gray-200">
        {/* File Upload Section */}
        <div className="mb-4 flex items-center space-x-4">
          <input
            type="file"
            accept=".pdf, .doc, .docx, .txt"
            onChange={handleFileChange}
          />
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleUpload}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg shadow-md hover:bg-blue-600"
          >
            Upload
          </motion.button>
        </div>

        {/* Chat Interface */}
        <h2 className="text-xl font-semibold text-blue-600 mb-2">
          Chat Interface:
        </h2>
        <div className="h-60 overflow-y-auto bg-gray-200 p-4 rounded-lg shadow-inner mb-4 border border-gray-400">
          {chatHistory.map((chat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3 }}
              className="mb-2"
            >
              <p className="text-right text-blue-700 font-semibold">
                User: {chat.user}
              </p>
              <p className="text-left bg-gradient-to-r from-blue-200 to-blue-300 p-3 rounded-lg text-blue-900 font-bold border border-blue-400 shadow-md">
                Bot: {chat.bot}
              </p>
            </motion.div>
          ))}
        </div>

        <div className="flex items-center space-x-2">
          <input
            type="text"
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            placeholder="Type your query..."
            className="flex-1 px-3 py-2 border rounded-lg shadow-sm focus:ring focus:ring-blue-200"
          />
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleChatSubmit}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg shadow-md hover:bg-blue-600"
          >
            Send
          </motion.button>
        </div>
      </div>
    </div>
  );
};

export default LegalAssistant;
