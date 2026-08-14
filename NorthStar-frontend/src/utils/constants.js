export const ORDER_STEPS = [
  'Order Placed',
  'Processing',
  'Shipped',
  'Delivered'
];

export const ORDER_STATUS = {
  PROCESSING: 'processing',
  SHIPPED: 'shipped',
  DELIVERED: 'delivered',
  CANCELLED: 'cancelled'
};

export const RETURN_REASONS = [
  { value: 'defective', label: 'Defective' },
  { value: 'wrong_size', label: 'Wrong size' },
  { value: 'changed_mind', label: 'Changed mind' }
];

export const RETURN_STATUS = {
  SUBMITTED: 'submitted',
  APPROVED: 'approved',
  REJECTED: 'rejected'
};

export const STOCK_STATUS = {
  IN_STOCK: 'in_stock',
  LOW_STOCK: 'low_stock',
  OUT_OF_STOCK: 'out_of_stock'
};