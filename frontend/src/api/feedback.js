import { axiosInstance } from "./axiosInstance";
  
  // Send feedback
  export const sendFeedback = async (data, userId) => {
      try {
          const token = localStorage.getItem("token");
          if (!token) {
              throw new Error("No token found, please log in.");
          }
  
          const response = await axiosInstance.post(
              "/feedback",
              {
                  ...data,
                  userId: userId,  
              },
              {
                  headers: {
                      Authorization: `Bearer ${token}`, 
                  },
              }
          );
          return response.data;
      } catch (error) {
          console.error("Feedback submission failed:", error);
          throw error;
      }
  };
  
  
  // Get feedbacks (all or user-specific)
  export const getFeedbacks = async (userId, isAllFeedback = false) => {
      try {
          const token = localStorage.getItem('token');  
          if (!token) {
              throw new Error("No access token found");
          }
  
          let url = '/feedback';
          if (isAllFeedback) {
              url = '/feedback/all';
          }
  
          const response = await axiosInstance.get(url, {
              headers: { Authorization: `Bearer ${token}` },
              params: isAllFeedback ? {} : { userId: userId },  
  
          });
  
          console.log("Fetched Feedbacks from API:", response.data);
  
          return response.data;  
      } catch (err) {
          console.error("Error fetching feedback:", err.message);
          throw err;  
      }
  };
  ;
  
  // Delete feedback
  export const deleteFeedback = async (feedbackId) => {
      try {
          const token = localStorage.getItem("token");
          if (!token) {
              throw new Error("No token found, please log in.");
          }
  
          const response = await axiosInstance.delete(
              `/feedback/${feedbackId}`,
              {
                  headers: {
                      Authorization: `Bearer ${token}`,
                  },
              }
          );
  
          return response.data;
      } catch (error) {
          console.error("Error deleting feedback:", error);
          throw error;
      }
  };