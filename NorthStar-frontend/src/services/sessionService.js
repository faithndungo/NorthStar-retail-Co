// src/services/sessionService.js
import { apiFetch } from './api.js';

/**
 * POST /api/accounts/session/
 * Creates or retrieves a guest session token.
 */
export async function createSession(email = '', phoneNumber = '') {
  return apiFetch('/accounts/session/', {
    method: 'POST',
    body: { email, phone_number: phoneNumber },
  });
}

/**
 * Backward compatibility alias if any component calls initSession
 */
export const initSession = createSession;