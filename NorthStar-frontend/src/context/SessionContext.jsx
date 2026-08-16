import { useEffect, useState } from 'react';
import { createSession } from '../services/sessionService.js';
import { SessionContext } from './sessionContext.js';

function makeLocalToken() {
  if (window.crypto && window.crypto.randomUUID) {
    return `guest-${window.crypto.randomUUID()}`;
  }
  return `guest-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

export function SessionProvider({ children }) {
  const [sessionToken, setSessionToken] = useState(
    () => sessionStorage.getItem('northstar_guest_token') || ''
  );
  const [sessionLoading, setSessionLoading] = useState(true);
  const [sessionWarning, setSessionWarning] = useState('');

  useEffect(() => {
    let active = true;

    async function initSession() {
      setSessionLoading(true);
      setSessionWarning('');
      const existing = sessionStorage.getItem('northstar_guest_token') || '';

      try {
        const data = await createSession(existing);
        const token = data.session_token || data.token || existing || makeLocalToken();
        if (!active) return;
        sessionStorage.setItem('northstar_guest_token', token);
        setSessionToken(token);
      } catch {
        if (!active) return;
        const token = existing || makeLocalToken();
        sessionStorage.setItem('northstar_guest_token', token);
        setSessionToken(token);
        setSessionWarning('Guest session API unavailable. Using local temporary token.');
      } finally {
        if (active) setSessionLoading(false);
      }
    }

    initSession();
    return () => { active = false; };
  }, []);

  return (
    <SessionContext.Provider value={{ sessionToken, sessionLoading, sessionWarning }}>
      {children}
    </SessionContext.Provider>
  );
}
