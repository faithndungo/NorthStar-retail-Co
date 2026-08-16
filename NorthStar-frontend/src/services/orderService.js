import { apiFetch } from './api.js';

/**
 * POST /api/orders/lookup/
 * Accepts order_number + customer_email, returns shipping status and tracking link.
 */
export async function lookupOrder({ order_number, customer_email }, token) {
  return apiFetch('/orders/lookup/', {
    method: 'POST',
    body: { order_number, customer_email },
    token
  });
}
