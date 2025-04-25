import React from "react";
import { useLocation } from "react-router-dom";
import AppRoutes from "./routes/AppRoutes";
import Header from "./components/Layout/Header";
import Footer from "./components/Layout/Footer";
import "./index.css";

const App = () => {
  const location = useLocation();
  const isChatbotPage = location.pathname === "/chatbot"; 

  return (
    <div className="flex flex-col min-h-screen">
      <Header /> {/* Show Header on all pages */}
      <div className="flex flex-1">
        <main className="flex-1 overflow-y-auto">
          <AppRoutes />
        </main>
      </div>
      {!isChatbotPage && <Footer />} {/* Hide Footer on chatbot page */}
    </div>
  );
};

export default App;
