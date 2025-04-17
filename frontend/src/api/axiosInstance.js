import axios from "axios";
 
 // Create an axios instance with baseURL
 const axiosInstance = axios.create({
     baseURL: "http://127.0.0.1:8000/api",
 });
 
 // The token will be set dynamically in the component instead of the axiosInstance
 const setAuthorizationToken = (token) => {
     if (token) {
         axiosInstance.defaults.headers.Authorization = `Bearer ${token}`;
     } else {
         console.warn("No auth token found! Requests may be unauthorized.");
     }
 };
 
 export { axiosInstance, setAuthorizationToken };