import { axiosInstance } from "./axiosInstance";
 
 // Login with email and password
 export const loginUser = async (email, password) => {
     try {
         const response = await axiosInstance.post("/auth/login", { email, password });
         return response.data;
     } catch (error) {
         console.error("Login failed:", error.response?.data || error.message);
         throw error;
     }
 };
 
 // Register a new user
 export const registerUser = async (userData) => {
     try {
         const response = await axiosInstance.post("/auth/register", userData);
         return response.data;
     } catch (error) {
         console.error("Registration failed:", error.response?.data || error.message);
         throw error;
     }
 };
 
 // Verify email with a code
 export const verifyEmail = async (email, verificationCode) => {
     try {
         const response = await axiosInstance.post("/auth/verify-email", { email, code: verificationCode });
         return response.data;
     } catch (error) {
         console.error("Email verification failed:", error.response?.data || error.message);
         throw error;
     }
 };
 
 // Login with Google OAuth token
 export const googleLogin = async (googleToken) => {
     try {
         const response = await axiosInstance.post("/auth/google-login", { token: googleToken });
         return response.data;
     } catch (error) {
         console.error("Google login failed:", error.response?.data || error.message);
         throw error;
     }
 };
 
 // Login with Microsoft OAuth token
 export const microsoftLogin = async (microsoftToken) => {
     try {
         const response = await axiosInstance.post("/auth/microsoft-login", { token: microsoftToken });
         return response.data;
     } catch (error) {
         console.error("Microsoft login failed:", error.response?.data || error.message);
         throw error;
     }
 };
 
 // Fetch the current user profile
 export const getUserProfile = async () => {
     try {
         const token = localStorage.getItem("token"); 
         if (!token) {
             throw new Error("No authentication token found.");
         }
 
         const response = await axiosInstance.get("/auth/me", {
             headers: {
                 Authorization: `Bearer ${token}`,
             },
         });
 
         return response.data;
     } catch (error) {
         console.error("Failed to fetch user profile:", error.response?.data || error.message);
         throw error;
     }
 };