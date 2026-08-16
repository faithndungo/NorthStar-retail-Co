import test from 'node:test';
import assert from 'node:assert/strict';

import { isValidEmail, validateOrderLookup } from './validators.js';
import { currentStepForStatus, normalizeStockStatus } from './formatters.js';

test('validates customer order lookup details', () => {
  assert.equal(isValidEmail('buyer@example.com'), true);
  assert.deepEqual(
    validateOrderLookup({ order_number: '', customer_email: 'bad' }),
    {
      order_number: 'Order number is required.',
      customer_email: 'Enter a valid email address.'
    }
  );
});

test('normalizes inventory and shipment statuses', () => {
  assert.equal(normalizeStockStatus('low_stock', 3).label, '3 Left');
  assert.equal(normalizeStockStatus('in_stock', 0).status, 'out_of_stock');
  assert.equal(currentStepForStatus('delivered'), 3);
});
