import React, { createContext, useContext, useState, useEffect } from 'react';
import { createSession } from '../services/sessionService';

const SessionContext = createContext();

export const SessionProvider = ({ children }) => {
  const [sessionToken, setSessionToken] = useState(
    localStorage.getItem('x_session_token') || ''
  );

  const initGuestSession = async (email = '', phone = '') => {
    try {
      const data = await createSession(email, phone);
      if (data?.session_token) {
        localStorage.setItem('x_session_token', data.session_token);
        setSessionToken(data.session_token);
      }
      return data;
    } catch (err) {
      console.error('Failed to initialize session:', err);
    }
  };

  useEffect(() => {
    if (!sessionToken) {
      initGuestSession();
    }
  }, []);

  return (
    <SessionContext.Provider value={{ sessionToken, initGuestSession }}>
      {children}
    </SessionContext.Provider>
  );
};

export const useSession = () => useContext(SessionContext);