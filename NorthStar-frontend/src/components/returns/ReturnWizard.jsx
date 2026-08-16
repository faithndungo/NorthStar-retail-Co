import { useState } from 'react';
import { useSession } from '../../context/sessionContext.js';
import {
  checkReturnEligibility,
  createReturnRequest
} from '../../services/returnService.js';
import { RETURN_REASONS } from '../../utils/constants.js';
import LoadingSkeleton from '../common/LoadingSkeleton.jsx';
import ErrorNotice from '../common/ErrorNotice.jsx';
import ReturnReceipt from './ReturnReceipt.jsx';

export default function ReturnWizard() {
  const { sessionToken } = useSession();

  const [step, setStep] = useState(1);
  const [form, setForm] = useState({ order_number: '', customer_email: '' });
  const [orderDetail, setOrderDetail] = useState(null);
  const [selectedItem, setSelectedItem] = useState('');
  const [reason, setReason] = useState('');
  const [agreed, setAgreed] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [returnData, setReturnData] = useState(null);

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  }

  function resetWizard() {
    setStep(1);
    setForm({ order_number: '', customer_email: '' });
    setOrderDetail(null);
    setSelectedItem('');
    setReason('');
    setAgreed(false);
    setError('');
    setReturnData(null);
  }

  async function handleEligibility(e) {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const eligibility = await checkReturnEligibility(
        {
          order_number: form.order_number.trim(),
          customer_email: form.customer_email.trim()
        },
        sessionToken
      );

      // Backend returns business-rule result with eligible flag
      if (eligibility.eligible === false) {
        setError(
          eligibility.message || 'This order is not eligible for return.'
        );
        return;
      }

      const order = eligibility.order;
      if (!order) throw new Error('The API did not return eligible order details.');

      setOrderDetail(order);
      setSelectedItem(order.items?.[0]?.id || '');
      setStep(2);
    } catch (err) {
      setError(err.message || 'Unable to check return eligibility.');
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmitReturn(e) {
    e.preventDefault();
    if (!agreed) {
      setError('Please agree to the return policy.');
      return;
    }
    setLoading(true);
    setError('');

    try {
      const payload = {
        order: orderDetail.order_number,
        order_number: orderDetail.order_number,
        customer_email: form.customer_email.trim(),
        reason,
        item_id: selectedItem || undefined
      };

      const response = await createReturnRequest(payload, sessionToken);
      setReturnData(response);
      setStep(4);
    } catch (err) {
      setError(err.message || 'Unable to create return request.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="card" aria-label="Returns and refunds">
      <h2>Start a Return</h2>
      <p className="wizard-steps">Step {step} of 4</p>

      <ErrorNotice message={error} />
      {loading && <LoadingSkeleton lines={3} />}

      {step === 1 && !loading && (
        <form className="form-grid" onSubmit={handleEligibility}>
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
          <button type="submit">Check return eligibility</button>
        </form>
      )}

      {step === 2 && orderDetail && !loading && (
        <form
          className="form-grid"
          onSubmit={(e) => {
            e.preventDefault();
            if (!reason) {
              setError('Select a return reason.');
              return;
            }
            setError('');
            setStep(3);
          }}
        >
          {orderDetail.items && orderDetail.items.length > 0 ? (
            <label>
              Item to return
              <select
                value={selectedItem}
                onChange={(e) => setSelectedItem(e.target.value)}
              >
                {orderDetail.items.map((item, idx) => {
                  const val = item.id || item.sku || `item-${idx}`;
                  const label =
                    item.title || item.name || item.sku || `Item ${idx + 1}`;
                  return (
                    <option key={val} value={val}>
                      {label}
                    </option>
                  );
                })}
              </select>
            </label>
          ) : (
            <div className="notice">
              No item list was returned. Continue to return the whole order.
            </div>
          )}

          <label>
            Reason
            <select
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              required
            >
              <option value="">Select a reason</option>
              {RETURN_REASONS.map((r) => (
                <option key={r.value} value={r.value}>
                  {r.label}
                </option>
              ))}
            </select>
          </label>

          <div className="action-row">
            <button
              type="button"
              className="button secondary"
              onClick={() => {
                setError('');
                setStep(1);
              }}
            >
              Back
            </button>
            <button type="submit" disabled={!reason}>
              Continue
            </button>
          </div>
        </form>
      )}

      {step === 3 && orderDetail && !loading && (
        <form className="form-grid" onSubmit={handleSubmitReturn}>
          <dl className="result-meta">
            <div><dt>Order</dt><dd>{orderDetail.order_number}</dd></div>
            <div><dt>Item</dt><dd>{selectedItem || 'Whole order'}</dd></div>
            <div>
              <dt>Reason</dt>
              <dd>
                {RETURN_REASONS.find((r) => r.value === reason)?.label || reason}
              </dd>
            </div>
          </dl>

          <label className="checkbox">
            <input
              type="checkbox"
              checked={agreed}
              onChange={(e) => setAgreed(e.target.checked)}
            />
            I agree to the return policy and understand refund eligibility.
          </label>

          <div className="action-row">
            <button
              type="button"
              className="button secondary"
              onClick={() => {
                setError('');
                setStep(2);
              }}
            >
              Back
            </button>
            <button type="submit" disabled={!agreed || loading}>
              {loading ? 'Submitting…' : 'Submit return'}
            </button>
          </div>
        </form>
      )}

      {step === 4 && returnData && !loading && (
        <ReturnReceipt
          returnData={returnData}
          orderNumber={orderDetail.order_number}
          reason={reason}
          onReset={resetWizard}
        />
      )}
    </section>
  );
}
