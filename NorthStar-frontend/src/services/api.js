// src/services/api.js

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000/api';
export const API_BASE_URL = API_BASE;

function buildQuery(params) {
  const qs = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
    .join('&');
  return qs ? `?${qs}` : '';
}

async function apiFetch(path, { method = 'GET', body, token } = {}) {
  const headers = { Accept: 'application/json' };
  if (body !== undefined) headers['Content-Type'] = 'application/json';
  if (token) headers['X-Session-Token'] = token;

  let response;
  try {
    response = await fetch(`${API_BASE}${path}`, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body)
    });
  } catch {
    throw new Error('Network error. Check that the Northstar API is reachable.');
  }

  let payload = {};
  try {
    payload = await response.json();
  } catch {
    payload = {};
  }

  if (!response.ok) {
    const detail =
      payload?.error?.message ||
      payload.detail ||
      payload.message ||
      payload.non_field_errors;

    const message = Array.isArray(detail)
      ? detail.join(' ')
      : detail || `Request failed with status ${response.status}.`;

    const err = new Error(message);
    err.status = response.status;
    err.payload = payload;
    throw err;
  }

  return payload;
}

export { apiFetch, buildQuery };