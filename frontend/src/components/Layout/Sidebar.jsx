import { useContext, useState, useEffect, useRef } from "react";
import { ChatContext } from "../../context/ChatContext";
import { X, Search } from "lucide-react";
import { useLocation } from "react-router-dom";

const Sidebar = ({ isOpen, toggleSidebar }) => {
  const { chatHistory = [] } = useContext(ChatContext);
  const location = useLocation();
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const searchInputRef = useRef(null);

  useEffect(() => {
    if (isSearchOpen) {
      setTimeout(() => searchInputRef.current?.focus(), 100);
    }
  }, [isSearchOpen]);

  // Show sidebar only on /chatbot page
  if (location.pathname !== "/chatbot") return null;

  return (
    <>
      <aside
        className={`fixed left-0 top-[4rem] h-[calc(100vh-4rem)] w-72 bg-white text-black shadow-lg border-r border-gray-300 
        transition-transform duration-300 ease-in-out z-50 overflow-y-auto custom-scrollbar ${isOpen ? "translate-x-0" : "-translate-x-80"}`}
      >
        <div className="flex justify-end items-center p-4 border-gray-300">
          <button onClick={() => setIsSearchOpen(true)} className="p-2 rounded-full hover:bg-gray-200 transition duration-300">
            <Search size={20} />
          </button>
        </div>
      </aside>

      {isSearchOpen && (
        <div
          className="fixed inset-0 flex justify-center items-center z-50 bg-black bg-opacity-30 backdrop-blur-sm"
          onClick={() => setIsSearchOpen(false)}
        >
          <div
            className="bg-white p-6 rounded-xl shadow-xl w-96 relative transform scale-95 animate-fadeIn"
            onClick={(e) => e.stopPropagation()} 
          >
            <div className="flex justify-between items-center border-b pb-3 mb-4">
              <input 
                type="text" 
                ref={searchInputRef}
                className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" 
                placeholder="Search chats..." 
              />
              <button onClick={() => setIsSearchOpen(false)} className="p-2 rounded-full hover:bg-gray-200 transition duration-300">
                <X size={20} />
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Sidebar;