import axios from "axios";

// Prefer explicitly set external URL (e.g., if bypassing Next.js proxy),
// otherwise fallback to empty string to use relative paths and Next.js rewrites on the client.
let API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || "";

const isServer = typeof window === "undefined";
if (isServer && !API_BASE_URL) {
  // During Server-Side Rendering (SSR), Axios requires an absolute URL.
  // We construct it using Vercel's system environment variable or fallback to localhost.
  const vercelUrl = process.env.VERCEL_URL || process.env.NEXT_PUBLIC_VERCEL_URL;
  API_BASE_URL = vercelUrl ? `https://${vercelUrl}` : "http://localhost:3000";
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
