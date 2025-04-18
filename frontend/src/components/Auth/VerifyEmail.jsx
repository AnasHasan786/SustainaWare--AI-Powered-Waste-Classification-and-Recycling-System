import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { verifyEmail } from "../../api/auth";
import { useAuth } from "../../context/AuthContext";

const VerifyEmail = () => {
    const [code, setCode] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();
    const { login } = useAuth();

    const email = localStorage.getItem("email");

    const handleVerification = async (e) => {
        e.preventDefault();
        setError("");
    
        if (!email) {
            setError("Email not found. Please sign up again.");
            return;
        }
    
        try {
            const response = await verifyEmail(email, code);
            console.log("Full verification response:", response);  
    
            if (!response || !response.access_token || !response.user_id) {
                throw new Error("Missing access_token or user_id.");
            }
    
            const { access_token, user_id, email: verifiedEmail } = response;
    
            localStorage.setItem("user", JSON.stringify({ user_id, email: verifiedEmail }));
            localStorage.setItem("token", access_token);
    
            // Log the user in
            login({ user_id, email: verifiedEmail }, access_token);
    
            navigate("/");
        } catch (err) {
            console.error("Verification error:", err.message);
            setError(err.message || "Verification failed. Try again.");
        }
    };
    
    
    

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4 mt-10">
            <div className="bg-white p-8 shadow-2xl rounded-2xl w-full max-w-md text-center">
                <h2 className="text-3xl font-extrabold mb-6 text-gray-800">Verify Your Email</h2>

                {error && <p className="text-red-600 bg-red-100 border border-red-400 p-2 rounded-lg mb-4">{error}</p>}

                <form onSubmit={handleVerification} className="space-y-5">
                    <div className="relative">
                        <input
                            type="text"
                            placeholder="Enter Verification Code"
                            value={code}
                            onChange={(e) => setCode(e.target.value)}
                            className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-green-500"
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="w-full bg-green-600 text-white p-3 rounded-lg font-semibold transition duration-300 ease-in-out hover:bg-green-700 hover:shadow-lg cursor-pointer"
                    >
                        Verify
                    </button>
                </form>
            </div>
        </div>
    );
};

export default VerifyEmail;
