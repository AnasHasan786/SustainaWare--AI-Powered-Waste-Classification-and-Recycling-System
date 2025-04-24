import React from "react";
import { Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import Chatbot from "../pages/Chatbot";
import Feedback from "../pages/Feedback";
import Account from "../pages/Account";
import NotFound from "../pages/NotFound";
import Register from "../components/Auth/Register";
import Login from "../components/Auth/Login"; 
import VerifyEmail from "../components/Auth/VerifyEmail";

const AppRoutes = () => {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/chatbot" element={<Chatbot />} />
            <Route path="/feedback" element={<Feedback />} /> 

            {/* Add Account Route */}
            <Route path="/account" element={<Account />} />

            {/* Add Register Route */}
            <Route path="/register" element={<Register />} />

            <Route path="/verify-email" element={<VerifyEmail />} />
            
            {/* Add Login Route */}
            <Route path="/login" element={<Login />} />

            <Route path="*" element={<NotFound />} />
        </Routes>
    );
};

export default AppRoutes;
