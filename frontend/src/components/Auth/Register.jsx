import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { axiosInstance, setAuthorizationToken } from "../../api/axiosInstance";
import { FcGoogle } from "react-icons/fc";
import { BsMicrosoft } from "react-icons/bs";
import { FaUser, FaEnvelope, FaLock } from "react-icons/fa";

const Register = () => {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState("");
    const { user, login, token } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        if (user) {
            navigate("/");  
        }
    }, [user, navigate]);

    useEffect(() => {
        if (token) {
            setAuthorizationToken(token);
        }
    }, [token]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
    
        if (password.length < 6) {
            setError("Password must be at least 6 characters long.");
            return;
        }
    
        if (password !== confirmPassword) {
            setError("Passwords do not match!");
            return;
        }
    
        try {
            const response = await axiosInstance.post("/auth/register", { name, email, password });
            localStorage.setItem("email", email);
            navigate("/verify-email");
        } catch (err) {
            console.error("Error during registration:", err);
            setError(err.response?.data?.message || "Registration failed. Try again.");
        }
    };

    const handleGoogleSignup = () => {
        window.location.href = "http://localhost:5000/auth/google";
    };

    const handleMicrosoftSignup = () => {
        window.location.href = "http://localhost:5000/auth/microsoft";
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4 mt-10">
            <div className="bg-white p-8 shadow-2xl rounded-2xl w-full max-w-md text-center">
                <h2 className="text-3xl font-extrabold mb-6 text-gray-800">Create an Account</h2>

                {error && <p className="text-red-600 bg-red-100 border border-red-400 p-2 rounded-lg mb-4">{error}</p>}

                <div autoComplete="off">
                    <input type="text" name="fake_username" style={{ display: "none" }} />

                    <form onSubmit={handleSubmit} className="space-y-5" autoComplete="off">
                        {/* Full Name Field */}
                        <div className="relative">
                            <FaUser className="absolute left-4 top-3 text-gray-500" />
                            <input
                                type="text"
                                placeholder="Full Name"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                className="w-full p-3 pl-10 border rounded-lg focus:ring-2 focus:ring-green-500"
                                required
                                autoComplete="off"
                                spellCheck="false"
                                name="name"
                            />
                        </div>

                        {/* Email Field */}
                        <div className="relative">
                            <FaEnvelope className="absolute left-4 top-3 text-gray-500" />
                            <input
                                type="email"
                                placeholder="Email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full p-3 pl-10 border rounded-lg focus:ring-2 focus:ring-green-500"
                                required
                                autoComplete="off"
                                spellCheck="false"
                                name="email"
                            />
                        </div>

                        {/* Password Field */}
                        <div className="relative">
                            <FaLock className="absolute left-4 top-3 text-gray-500" />
                            <input
                                type="password"
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full p-3 pl-10 border rounded-lg focus:ring-2 focus:ring-green-500"
                                required
                                autoComplete="new-password"
                                spellCheck="false"
                                name="new-password"
                            />
                        </div>

                        {/* Confirm Password Field */}
                        <div className="relative">
                            <FaLock className="absolute left-4 top-3 text-gray-500" />
                            <input
                                type="password"
                                placeholder="Confirm Password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                className="w-full p-3 pl-10 border rounded-lg focus:ring-2 focus:ring-green-500"
                                required
                                autoComplete="new-password"
                                spellCheck="false"
                                name="new-password-confirm"
                            />
                        </div>

                        {/* Register Button */}
                        <button type="submit" className="w-full bg-green-600 text-white p-3 rounded-lg font-semibold transition duration-300 ease-in-out hover:bg-green-700 hover:shadow-lg cursor-pointer">
                            Register
                        </button>
                    </form>
                </div>

                {/* Divider */}
                <div className="flex items-center my-6">
                    <div className="flex-grow h-px bg-gray-300"></div>
                    <span className="mx-4 text-gray-500">OR</span>
                    <div className="flex-grow h-px bg-gray-300"></div>
                </div>

                {/* Google Signup */}
                <button onClick={handleGoogleSignup} className="w-full flex items-center justify-center bg-white border border-gray-300 p-3 rounded-lg shadow-md transition duration-300 ease-in-out hover:shadow-lg hover:bg-gray-100 cursor-pointer">
                    <FcGoogle className="text-2xl mr-2" /> Sign up with Google
                </button>

                {/* Microsoft Signup */}
                <button onClick={handleMicrosoftSignup} className="w-full flex items-center justify-center bg-white border border-gray-300 p-3 rounded-lg shadow-md mt-2 transition duration-300 ease-in-out hover:shadow-lg hover:bg-gray-100 cursor-pointer">
                    <BsMicrosoft className="text-xl text-blue-700 mr-2" /> Sign up with Microsoft
                </button>

                {/* Login Link */}
                <p className="mt-4 text-gray-600">
                    Already have an account? <a href="/login" className="text-green-600 hover:underline">Login</a>
                </p>
            </div>
        </div>
    );
};

export default Register;
