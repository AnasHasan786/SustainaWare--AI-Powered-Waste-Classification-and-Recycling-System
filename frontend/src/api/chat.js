import { axiosInstance } from "./axiosInstance";
 
 export const sendChatMessage = async (message) => {
     try {
         const response = await axiosInstance.post("/chat", { message });
         return response.data;
     } catch (error) {
         console.error("Chat request failed:", error);
         throw error;
     }
 };
 
 export const getChatHistory = async () => {
     try {
         const response = await axiosInstance.get("/chat/history");
         return response.data;
     } catch(error) {
         console.error("Error fetching chat history:", error);
         throw error;
     }
 }