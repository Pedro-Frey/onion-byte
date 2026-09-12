import axios from 'axios';
import { sanitizeObject } from './security';
import { getToken } from './auth';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true // Important for CSRF or HttpOnly cookies if backend uses them
});

// Request interceptor
api.interceptors.request.use((config) => {
  // Always sanitize payloads to prevent XSS (skip form data types)
  if (config.data && !(config.data instanceof URLSearchParams) && !(config.data instanceof FormData)) {
    config.data = sanitizeObject(config.data);
  }

  // Get token (if using localStorage approach as requested for this demo)
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
}, (error) => {
  return Promise.reject(error);
});

// Response interceptor
api.interceptors.response.use((response) => {
  // Sanitize incoming data just in case
  if (response.data) {
    response.data = sanitizeObject(response.data);
  }
  return response;
}, (error) => {
  if (error.response && error.response.status === 401) {
    // [DEV MODE] Comentado para testes
    // if (typeof window !== 'undefined' && !window.location.pathname.includes('/login')) {
    //   window.location.href = '/login';
    // }
  }
  return Promise.reject(error);
});

export default api;
