export function isValidEmail(email) {
  return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(String(email || '').trim());
}

export function isRequired(value) {
  return String(value || '').trim().length > 0;
}

export function validateOrderLookup({ order_number, customer_email }) {
  const errors = {};
  if (!isRequired(order_number)) errors.order_number = 'Order number is required.';
  if (!isRequired(customer_email)) errors.customer_email = 'Email is required.';
  else if (!isValidEmail(customer_email)) errors.customer_email = 'Enter a valid email address.';
  return errors;
}

export function validateReturnForm({ reason, agreed }) {
  const errors = {};
  if (!isRequired(reason)) errors.reason = 'Select a return reason.';
  if (!agreed) errors.agreed = 'Please agree to the return policy.';
  return errors;
}

export function validateStockAlertEmail(email) {
  if (!isValidEmail(email)) return 'Enter a valid email address.';
  return '';
}