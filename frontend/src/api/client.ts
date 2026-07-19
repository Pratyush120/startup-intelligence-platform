import axios from "axios";

// Prefer explicitly set external URL (e.g., if bypassing Next.js proxy)
let API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || "";

const isServer = typeof window === "undefined";

if (isServer) {
  // During Server-Side Rendering (SSR), Axios requires an absolute URL.
  // We hit the backend directly (bypassing Next.js rewrites) to avoid unhandled proxy socket errors.
  API_BASE_URL = API_BASE_URL || "http://127.0.0.1:8000";
}

export const apiClient = axios.create({
  baseURL: API_BASE_URL ? `${API_BASE_URL}/api/v1` : "/api/v1",
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
