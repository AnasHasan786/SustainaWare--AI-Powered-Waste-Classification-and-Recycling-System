import { useState, useRef } from "react";
import { UploadCloud, SendHorizonal, XCircle } from "lucide-react";

const Chatbox = ({ onSend }) => {
  const [message, setMessage] = useState("");
  const [image, setImage] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(URL.createObjectURL(file));
      setImageFile(file);
    }
  };

  const handleSendClick = async () => {
    if (!message.trim() && !image) return;
    setLoading(true);
    await onSend({ text: message.trim(), image, imageFile });
    setLoading(false);
    setMessage("");
    setImage(null);
    setImageFile(null);
  };

  return (
    <div className="relative max-w-2xl mx-auto bg-[#2D2D2D] p-3 shadow-lg rounded-full flex items-center space-x-4 px-6">
      {/* Image Upload Button */}
      <button className="text-gray-400 hover:text-white cursor-pointer" onClick={() => fileInputRef.current.click()}>
        <UploadCloud className="w-6 h-6" />
      </button>
      <input type="file" accept="image/*" className="hidden" ref={fileInputRef} onChange={handleFileChange} />

      {/* Image Preview */}
      {image && (
        <div className="relative flex items-center">
          <img src={image} alt="Preview" className="w-12 h-12 object-cover rounded-md shadow-md border border-gray-300" />
          <button
            className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1"
            onClick={() => {
              setImage(null);
              setImageFile(null);
            }}
          >
            <XCircle className="w-5 h-5" />
          </button>
        </div>
      )}

      {/* Message Input */}
      <input
        type="text"
        className="flex-grow h-12 px-4 bg-transparent text-white placeholder-gray-400 outline-none"
        placeholder="Ask anything..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSendClick()}
      />

      {/* Send Button */}
      <button
        className="bg-white text-gray-400 hover:text-white h-12 w-12 flex items-center justify-center rounded-full hover:bg-gray-300 disabled:bg-gray-500 cursor-pointer"
        onClick={handleSendClick}
        disabled={(!message.trim() && !image) || loading}
      >
        {loading ? <span className="animate-spin">⏳</span> : <SendHorizonal className="w-6 h-6" />}
      </button>
    </div>
  );
};

export default Chatbox;
