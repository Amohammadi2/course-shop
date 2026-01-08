"use client";
import { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const initializeAuth = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        try {
          const { data } = await axios.get('/api/me/');
          setUser(data);
        } catch (error) {
          console.error('Failed to fetch user', error);
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
        }
      }
      setLoading(false);
    };
    initializeAuth();
  }, []);

  const login = async (username, password) => {
    try {
      const { data } = await axios.post('/api/auth/token/', { username, password });
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`;
      const { data: userData } = await axios.get('/api/me/');
      setUser(userData);
      router.push('/dashboard');
    } catch (error) {
      console.error('Login failed', error);
      throw error
    }
  };

  const signup = async (userData) => {
    try {
      await axios.post('/api/register/', userData);
      await login(userData.username, userData.password);
    } catch (error) {
      console.error('Signup failed', error);
      throw error
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
    router.push('/');
  };

  axios.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config;
      if (error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        try {
          const refreshToken = localStorage.getItem('refresh_token');
          const { data } = await axios.post('/api/auth/token/refresh/', { refresh: refreshToken });
          localStorage.setItem('access_token', data.access);
          axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`;
          originalRequest.headers['Authorization'] = `Bearer ${data.access}`;
          return axios(originalRequest);
        } catch (error) {
          logout();
        }
      }
      return Promise.reject(error);
    }
  );

  return (
    (<AuthContext.Provider value={{ user, login, signup, logout, loading }}>
      {children}
    </AuthContext.Provider>)
  );
};

export const useAuth = () => useContext(AuthContext);
