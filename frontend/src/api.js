import axios from "axios";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000",
});

// Automatically attach Bearer token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = "Bearer " + token;
  }
  return config;
});

// Handle expired/invalid tokens globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem("token");
      // Only redirect if not already on login page
      if (!window.location.pathname.includes("/login")) {
        alert("Your session has expired. Please log in again.");
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;