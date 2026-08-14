export function formatDate(dateString) {
  if (!dateString) return '—';
  const d = new Date(dateString);
  if (Number.isNaN(d.getTime())) return dateString;
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
}

export function formatOrderStatus(status) {
  const map = {
    processing: 'Processing',
    shipped: 'Shipped',
    delivered: 'Delivered',
    cancelled: 'Cancelled'
  };
  return map[String(status || '').toLowerCase()] || status;
}

/**
 * Normalizes the backend stock response into a UI badge.
 * Backend is the source of truth for stock_status; available_count is
 * used for the "N Left" label per the requirements document.
 */
export function normalizeStockStatus(status, availableCount) {
  const s = String(status || '').toLowerCase();
  const count = Number(availableCount ?? 0);

  if (s === 'out_of_stock' || count === 0) {
    return { status: 'out_of_stock', label: 'Out of Stock', className: 'badge-out' };
  }

  if (s === 'low_stock') {
    return {
      status: 'low_stock',
      label: count > 0 ? `${count} Left` : 'Out of Stock',
      className: count > 0 ? 'badge-low' : 'badge-out'
    };
  }

  return { status: 'in_stock', label: 'In Stock', className: 'badge-in' };
}

export function currentStepForStatus(status) {
  const s = String(status || '').toLowerCase();
  if (s.includes('deliver')) return 3;
  if (s.includes('ship')) return 2;
  if (s.includes('process')) return 1;
  return 0;
}