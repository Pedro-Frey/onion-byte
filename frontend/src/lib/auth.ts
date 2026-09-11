import api from './api';
import { encryptToken, decryptToken } from './security';
import Cookies from 'js-cookie';

const TOKEN_KEY = 'ob_auth_token';

export const setToken = (token: string) => {
  if (typeof window !== 'undefined') {
    // Store encrypted in localStorage
    localStorage.setItem(TOKEN_KEY, encryptToken(token));
    // Store in cookie for middleware to read
    // secure: true only in production (HTTPS), false in dev (HTTP localhost)
    const isSecure = window.location.protocol === 'https:';
    Cookies.set(TOKEN_KEY, token, { secure: isSecure, sameSite: 'strict' });
  }
};

export const getToken = (): string | null => {
  if (typeof window !== 'undefined') {
    const encrypted = localStorage.getItem(TOKEN_KEY);
    return encrypted ? decryptToken(encrypted) : null;
  }
  return null;
};

export const clearToken = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(TOKEN_KEY);
    Cookies.remove(TOKEN_KEY);
  }
};

export const isAuthenticated = (): boolean => {
  return !!getToken();
};

export const login = async (email: string, password: string) => {
  const response = await api.post('/auth/login', {
    email,
    password
  });
  
  if (response.data && response.data.access_token) {
    setToken(response.data.access_token);
  }
  return response.data;
};

export const register = async (email: string, password: string, company_name: string) => {
  const response = await api.post('/auth/register', {
    email,
    password,
    company_name
  });
  return response.data;
};

export const logout = () => {
  clearToken();
  if (typeof window !== 'undefined') {
    window.location.href = '/login';
  }
};
