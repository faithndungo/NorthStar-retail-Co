import { apiFetch } from './api.js';

/**
 * POST /api/accounts/session/
 * Generates or verifies a temporary guest session token.
 */
export async function createSession(existingToken) {
  return apiFetch('/accounts/session/', {
    method: 'POST',
    body: existingToken ? { session_token: existingToken } : {}
  });
}