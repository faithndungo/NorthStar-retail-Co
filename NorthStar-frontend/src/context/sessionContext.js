import { createContext, useContext } from 'react';

export const SessionContext = createContext({
  sessionToken: '',
  sessionLoading: true,
  sessionWarning: ''
});

export function useSession() {
  return useContext(SessionContext);
}
