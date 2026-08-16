import { useState } from 'react';
import { useSession } from '../../context/sessionContext.js';
import { lookupOrder } from '../../services/orderService.js';
import { validateOrderLookup } from '../../utils/validators.js';
import { currentStepForStatus, formatDate } from '../../utils/formatters.js';
import LoadingSkeleton from '../common/LoadingSkeleton.jsx';
import ErrorNotice from '../common/ErrorNotice.jsx';
import ProgressSteps from './ProgressSteps.jsx';

export default function OrderStatusLookup() {
  const { sessionToken } = useSession();
  const [form, setForm] = useState({ order_number: '', customer_email: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [order, setOrder] = useState(null);

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setOrder(null);

    const errors = validateOrderLookup(form);
    if (Object.keys(errors).length > 0) {
      setError(Object.values(errors).join(' '));
      return;
    }

    setLoading(true);
    try {
      const lookupResult = await lookupOrder(
        {
          order_number: form.order_number.trim(),
          customer_email: form.customer_email.trim()
        },
        sessionToken
      );

      setOrder(lookupResult);
    } catch (err) {
      setError(err.message || 'Unable to find this order.');
    } finally {
      setLoading(false);
    }
  }

  const status = String(order?.status || '').toLowerCase();
  const cancelled = status === 'cancelled';
  const currentStep = currentStepForStatus(status);

  const trackingUrl =
    order?.tracking_url || '';
  const carrier =
    order?.tracking_carrier || '';
  const estimated = order?.estimated_delivery || '';
  const items = order?.items || [];

  return (
    <section className="card" aria-label="Order status lookup">
      <h2>Order Status</h2>
      <p>Check where your order is without opening a support ticket.</p>

      <form className="form-grid" onSubmit={handleSubmit}>
        <label>
          Order number
          <input
            name="order_number"
            value={form.order_number}
            onChange={handleChange}
            placeholder="e.g. NS-10023"
            required
          />
        </label>
        <label>
          Email used on the order
          <input
            type="email"
            name="customer_email"
            value={form.customer_email}
            onChange={handleChange}
            placeholder="you@example.com"
            required
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? 'Checking…' : 'Track order'}
        </button>
      </form>

      {loading && <LoadingSkeleton lines={4} />}
      <ErrorNotice message={error} />

      {order && !loading && (
        <div className="result">
          {cancelled ? (
            <div className="notice warning">
              This order is cancelled and will not show shipping milestones.
            </div>
          ) : (
            <ProgressSteps currentStep={currentStep} />
          )}

          <dl className="result-meta">
            {carrier && (
              <div><dt>Carrier</dt><dd>{carrier}</dd></div>
            )}
            {estimated && (
              <div><dt>Estimated delivery</dt><dd>{formatDate(estimated)}</dd></div>
            )}
            {trackingUrl && (
              <div>
                <dt>Tracking</dt>
                <dd>
                  <a href={trackingUrl} target="_blank" rel="noreferrer">
                    Track package
                  </a>
                </dd>
              </div>
            )}
          </dl>

          {items.length > 0 && (
            <div className="items">
              <h3>Items</h3>
              <ul>
                {items.map((item, idx) => (
                  <li key={item.id || idx}>
                    {item.title || item.name || item.sku || `Item ${idx + 1}`}
                    {item.quantity ? ` × ${item.quantity}` : ''}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </section>
  );
}
