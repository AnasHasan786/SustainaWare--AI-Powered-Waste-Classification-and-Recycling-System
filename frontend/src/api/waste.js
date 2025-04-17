import { axiosInstance } from "./axiosInstance";
 
 const getAuthHeaders = () => {
     const token = localStorage.getItem("token");
     if (!token) throw new Error("Authentication token not found. Please log in.");
     return { Authorization: `Bearer ${token}` };
 };
 
 export const uploadWasteImage = async (imageFile) => {
     try {
         const formData = new FormData();
         formData.append("file", imageFile);
 
         const response = await axiosInstance.post("/waste/classify", formData, {
             headers: { 
                 "Content-Type": "multipart/form-data",
                 ...getAuthHeaders()
             },
         });
 
         return response.data;
     } catch (error) {
         console.error("Error uploading waste image:", error.response?.data || error.message);
         throw error;
     }
 };
 
 export const getWasteHistory = async () => {
     try {
         const response = await axiosInstance.get("/api/waste/history", {
             headers: getAuthHeaders()
         });
         return response.data;
     } catch (error) {
         console.error("Error fetching waste history:", error.response?.data || error.message);
         throw error;
     }
 };
 
 export const sendTextQuery = async (text) => {
     try {
         const response = await axiosInstance.post("/nlp/predict", { text }, {
             headers: getAuthHeaders()
         });
         return response.data;
     } catch (error) {
         console.error("Error sending text query:", error.response?.data || error.message);
         throw error;
     }
 };