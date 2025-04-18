import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { axiosInstance, setAuthorizationToken } from "../../api/axiosInstance"; 
import { Link } from "react-router-dom";
import { Loader2, Mail, Lock } from "lucide-react";
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";
import { MsalProvider, useMsal } from "@azure/msal-react";
import { msalInstance } from "../../config/msalConfig";
import { googleLogin, microsoftLogin } from "../../api/auth";

const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const { login } = useAuth();
    const navigate = useNavigate();
    const { instance } = useMsal();

    useEffect(() => {
        setTimeout(() => {
            document.querySelector("input[type='email']")?.setAttribute("autocomplete", "off");
            document.querySelector("input[type='password']")?.setAttribute("autocomplete", "new-password");
        }, 500);
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            const response = await axiosInstance.post("/auth/login", { email, password }); 
            const { token, user } = response.data;

            setAuthorizationToken(token);

            localStorage.setItem("token", token);
            localStorage.setItem("user", JSON.stringify(user));

            login(user, token); 
            navigate("/"); 
        } catch (err) {
            console.error("Login failed:", err); 
            setError(err.response?.data?.message || "Login failed. Try again.");
        } finally {
            setLoading(false);
        }
    };

    const handleGoogleLogin = async (credentialResponse) => {
        setLoading(true);
        try {
            const userData = await googleLogin(credentialResponse.credential);
            const { token, user } = userData;

            setAuthorizationToken(token);

            localStorage.setItem("token", token);
            localStorage.setItem("user", JSON.stringify(user));

            login(user, token);
            navigate("/dashboard");
        } catch (err) {
            setError("Google Login failed. Try again.");
        } finally {
            setLoading(false);
        }
    };

    const handleMicrosoftLogin = async () => {
        setLoading(true);
        try {
            const loginResponse = await instance.loginPopup({ scopes: ["openid", "profile", "email"] });
            const userData = await microsoftLogin(loginResponse.idToken);
            const { token, user } = userData;

            setAuthorizationToken(token);

            localStorage.setItem("token", token);
            localStorage.setItem("user", JSON.stringify(user));

            login(user, token);
            navigate("/dashboard");
        } catch (err) {
            setError("Microsoft Login failed. Try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <GoogleOAuthProvider clientId={clientId}>
            <MsalProvider instance={msalInstance}>
                <div className="flex items-center justify-center min-h-screen bg-gray-100 p-4">
                    <div className="relative bg-white rounded-2xl p-10 w-full max-w-md border border-gray-300">
                        <div className="flex justify-center mb-5">
                            <img src="/logo.svg" alt="Brand Logo" className="h-12" />
                        </div>

                        <h2 className="text-3xl font-semibold text-center text-gray-900">Welcome Back!</h2>
                        <p className="text-center text-gray-600 mb-6">Log in to continue</p>

                        {error && <p className="text-red-500 text-center mb-4">{error}</p>}

                        <form onSubmit={handleSubmit} className="space-y-5" autoComplete="off">
                            <input type="text" name="fakeuser" style={{ display: "none" }} />
                            <input type="password" name="fakepassword" style={{ display: "none" }} />

                            <div className="relative">
                                <Mail className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-500" />
                                <input
                                    type="email"
                                    name="user_email_123"
                                    placeholder="Email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="w-full pl-12 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none shadow-sm"
                                    autoComplete="email"
                                    required
                                />
                            </div>
                            <div className="relative">
                                <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-500" />
                                <input
                                    type="password"
                                    name="user_pass_123"
                                    placeholder="Password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="w-full pl-12 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none shadow-sm"
                                    autoComplete="new-password"
                                    required
                                />
                            </div>

                            <button
                                type="submit"
                                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg flex justify-center items-center gap-2 transition-all duration-300 shadow-md active:scale-95 cursor-pointer"
                                disabled={loading}
                            >
                                {loading ? <Loader2 className="animate-spin w-5 h-5" /> : "Login"}
                            </button>
                        </form>

                        <div className="mt-4 text-center text-gray-700">
                            <p>
                                Don't have an account? <Link to="/register" className="text-blue-600 hover:underline">Register</Link>
                            </p>
                            <p className="mt-1">
                                <Link to="/forgot-password" className="text-blue-600 hover:underline">Forgot Password?</Link>
                            </p>
                        </div>

                        <div className="mt-6">
                            <p className="text-gray-600 text-center text-sm mb-3">Or log in with</p>
                            <div className="flex flex-col space-y-3">
                                <GoogleLogin onSuccess={handleGoogleLogin} onError={() => setError("Google Login Failed")} />
                                <button
                                    onClick={handleMicrosoftLogin}
                                    className="w-full bg-gray-900 text-white py-3 rounded-lg hover:bg-gray-800 transition-all duration-300 shadow-md cursor-pointer"
                                >
                                    Login with Microsoft
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </MsalProvider>
        </GoogleOAuthProvider>
    );
};

export default Login;
