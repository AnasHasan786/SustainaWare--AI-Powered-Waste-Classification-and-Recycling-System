import { useState, useContext, useEffect, useRef } from "react";
import { ChatContext } from "../context/ChatContext";
import Chatbox from "../components/Chat/Chatbox";
import { uploadWasteImage, sendTextQuery } from "../api/waste";
import parse from "html-react-parser";

const Chatbot = () => {
  const { messages, addMessage } = useContext(ChatContext);
  const [botTyping, setBotTyping] = useState(false);
  const [currentMessage, setCurrentMessage] = useState("");
  const chatContainerRef = useRef(null);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTo({
        top: chatContainerRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [messages, botTyping, currentMessage]);

  const handleSend = async ({ text, image, imageFile }) => {
    if (text) {
      addMessage({ text, sender: "user" });
      try {
        setBotTyping(true);
        const response = await sendTextQuery(text);
        typeMessage(response?.response || "❌ No response received.");
      } catch (error) {
        setBotTyping(false);
        addMessage({ text: "❌ Failed to process text query.", sender: "bot" });
      }
    }

    if (imageFile) {
      addMessage({ image, sender: "user" });
      try {
        setBotTyping(true);
        const response = await uploadWasteImage(imageFile);
        console.log("API Response:", response);

        const classification = response.classification?.[0];
        if (classification) {
          const recyclingSteps = classification.recycling_instructions
            .map(
              (step) =>
                `<p><strong>Step ${step.step}: ${step.title}</strong></p>
               <p>${step.description}</p>`
            )
            .join("");

          const decompositionDetails = `
            <div style="overflow-x: auto;">
              <table style="width: 100%; border-collapse: collapse; border: 1px solid #ccc; text-align: center; max-width: 100%;">
                <thead>
                  <tr style="background-color: #f3f3f3; color: #333;">
                    <th style="padding: 10px; border: 1px solid #ccc;">Method</th>
                    <th style="padding: 10px; border: 1px solid #ccc;">Time</th>
                    <th style="padding: 10px; border: 1px solid #ccc;">Process</th>
                    <th style="padding: 10px; border: 1px solid #ccc;">Impact</th>
                    <th style="padding: 10px; border: 1px solid #ccc;">Recyclability</th>
                    <th style="padding: 10px; border: 1px solid #ccc;">Factors</th>
                  </tr>
                </thead>
                <tbody>
                  ${Object.entries(classification.decomposition_methods)
              .map(
                ([method, details]) => `
                        <tr style="background-color: #fafafa;">
                          <td style="padding: 8px; border: 1px solid #ccc; word-break: break-word;">${method.charAt(0).toUpperCase() + method.slice(1)}</td>
                          <td style="padding: 8px; border: 1px solid #ccc;">${details.time}</td>
                          <td style="padding: 8px; border: 1px solid #ccc; word-break: break-word;">${details.process}</td>
                          <td style="padding: 8px; border: 1px solid #ccc; word-break: break-word;">${details.impact}</td>
                          <td style="padding: 8px; border: 1px solid #ccc;">${details.recyclability}</td>
                          <td style="padding: 8px; border: 1px solid #ccc; word-break: break-word;">${details.factors}</td>
                        </tr>
                      `
              )
              .join("")}
                </tbody>
              </table>
            </div>
          `;

          const fullMessage = `
            <div style="text-align: left; word-break: break-word;">
              <b>🗑 Waste Name:</b> ${classification.waste_name}<br>
              <b>📂 Category:</b> ${classification.category}<br>
              <b>🎯 Confidence:</b> ${(classification.confidence * 100).toFixed(2)}%<br>
              <b>⚖ Estimated Weight:</b> ${classification.estimated_weight}g<br><br>
              <b>♻ Recycling Instructions:</b><br><br>${recyclingSteps}<br><br>
              <b>🕰 Decomposition Methods:</b><br><br>${decompositionDetails}
            </div>
          `;

          typeMessage(fullMessage);
        } else {
          setBotTyping(false);
          addMessage({ text: "Classification failed. No data received.", sender: "bot" });
        }
      } catch (error) {
        console.error("Classification Error:", error);
        setBotTyping(false);
        addMessage({ text: "Failed to classify waste.", sender: "bot" });
      }
    }
  };

  const typeMessage = (fullMessage) => {
    setBotTyping(true);

    const tableRegex = /(<table.*?>.*?<\/table>)/s;
    const tableMatch = fullMessage.match(tableRegex);
    const tableContent = tableMatch ? tableMatch[0] : "";
    let textContent = tableMatch ? fullMessage.replace(tableRegex, "") : fullMessage;

    let index = 0;
    let tempMessage = "";
    const typingInterval = setInterval(() => {
      if (index < textContent.length) {
        tempMessage += textContent[index];
        index++;
        setCurrentMessage(tempMessage);
      } else {
        clearInterval(typingInterval);
        setCurrentMessage("");
        setBotTyping(false);
        addMessage({ text: textContent + tableContent, sender: "bot" });
      }
    }, 1);
  };

  return (
    <div className="relative flex h-[calc(107vh-60px)] bg-white text-black overflow-hidden">

      {/* Chat container (Ensures scrolling happens inside Chatbot) */}
      <div className="flex flex-col flex-grow overflow-y-auto">

        <div ref={chatContainerRef} className="flex-grow overflow-y-auto px-6 py-4 mt-16 pb-4 max-h-[calc(100vh-140px)]">
          {messages.map((msg, index) => (
            <div key={index} className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"} my-2`}>
              {msg.image && (
                <img src={msg.image} alt="Uploaded" className="max-w-[200px] h-auto rounded-md shadow-md mr-3 mb-2" />
              )}
              {msg.text && (
                <div className={`p-3 rounded-lg shadow-md max-w-[75%] text-justify ${msg.sender === "user" ? "bg-blue-500 text-white" : "bg-gray-200 text-black"}`}>
                  {parse(msg.text)}
                </div>
              )}
            </div>
          ))}

          {botTyping && (
            <div className="flex justify-start">
              <div className={`p-3 bg-gray-200 text-black rounded-lg shadow-md max-w-[75%] ${currentMessage ? "" : "animate-pulse"}`}>
                {parse(currentMessage) || "⏳ Generating response..."}
              </div>
            </div>
          )}
        </div>

        <div className="w-full bg-white p-4 shadow-lg">
          <Chatbox onSend={handleSend} />
        </div>
      </div>
    </div>
  );
};

export default Chatbot;