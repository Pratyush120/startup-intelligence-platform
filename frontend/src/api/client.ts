import axios from "axios";

export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || "/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Global error handling can be added here
    console.error("API Error:", error.response?.data || error.message);
    return Promise.reject(error);
  }
);
