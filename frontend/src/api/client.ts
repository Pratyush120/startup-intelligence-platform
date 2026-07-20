import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

if (!API_BASE_URL) {
  throw new Error("Configuration Error: NEXT_PUBLIC_API_BASE_URL is missing. Please set it in your environment variables.");
}
export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
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
