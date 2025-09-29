// API Configuration for different environments
const API_CONFIG = {
  development: {
    baseURL: 'http://localhost:5000',
    timeout: 30000
  },
  production: {
    baseURL: process.env.REACT_APP_API_URL || 'https://kolam-art-backend.onrender.com',
    timeout: 30000
  }
};

// Get current environment
const environment = process.env.NODE_ENV || 'development';

// Export current config
export const API_BASE_URL = API_CONFIG[environment].baseURL;
export const API_TIMEOUT = API_CONFIG[environment].timeout;

// Helper function to get full API URL
export const getApiUrl = (endpoint) => {
  const baseUrl = API_BASE_URL.endsWith('/') ? API_BASE_URL.slice(0, -1) : API_BASE_URL;
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  return `${baseUrl}${cleanEndpoint}`;
};

export default API_CONFIG[environment];
