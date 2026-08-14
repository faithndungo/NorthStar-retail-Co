import { apiFetch, buildQuery } from './api.js';

/**
 * GET /api/inventory/products/
 * Returns the product catalog with variants so the frontend can render
 * the size/color picker required by the StockChecker spec.
 *
 * NOTE: The requirements document defines Product and ProductVariant models
 * but does not define a catalog listing endpoint. The backend must expose
 * this endpoint (see shared JSON contract) or the variant picker cannot
 * be populated dynamically.
 */
export async function getProducts(token) {
  const data = await apiFetch('/inventory/products/', { token });
  if (Array.isArray(data)) return data;
  return data.products || data.results || [];
}

/**
 * GET /api/inventory/check/?product_id=&variant=
 * Returns stock status (in_stock | low_stock | out_of_stock) and available count.
 * size/color are sent as fallback identifiers when variant id is not yet resolved.
 */
export async function checkInventory({ product_id, variant, size, color }, token) {
  const query = buildQuery({ product_id, variant, size, color });
  return apiFetch(`/inventory/check/${query}`, { token });
}

/**
 * POST /api/inventory/alerts/
 * Captures user email for restock notifications (StockAlert model).
 */
export async function subscribeStockAlert({ variant, email }, token) {
  return apiFetch('/inventory/alerts/', {
    method: 'POST',
    body: { variant, email },
    token
  });
}