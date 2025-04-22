import { createContext, useState } from "react";

export const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState([]);

  const addMessage = (message) => {
    setMessages((prevMessages) => [...prevMessages, message]);
    return messages.length; 
  };

  const updateLastMessage = (messageId, newText) => {
    setMessages((prevMessages) =>
      prevMessages.map((msg, index) =>
        index === messageId ? { ...msg, text: newText } : msg
      )
    );
  };

  return (
    <ChatContext.Provider value={{ messages, addMessage, updateLastMessage }}>
      {children}
    </ChatContext.Provider>
  );
};
