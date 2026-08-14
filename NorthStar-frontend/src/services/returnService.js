import { apiFetch } from './api.js';

/**
 * POST /api/returns/eligibility/
 * Validates order date against ReturnPolicy (return_window_days).
 */
export async function checkReturnEligibility({ order_number, customer_email }, token) {
  return apiFetch('/returns/eligibility/', {
    method: 'POST',
    body: { order_number, customer_email },
    token
  });
}

/**
 * POST /api/returns/requests/
 * Creates a ReturnRequest and returns the downloadable shipping label payload.
 */
export async function createReturnRequest(payload, token) {
  return apiFetch('/returns/requests/', {
    method: 'POST',
    body: payload,
    token
  });
}