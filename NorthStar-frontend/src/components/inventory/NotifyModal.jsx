import { useState } from 'react';
import Modal from '../common/Modal.jsx';
import { subscribeStockAlert } from '../../services/inventoryService.js';
import { useSession } from '../../context/sessionContext.js';
import { validateStockAlertEmail } from '../../utils/validators.js';

export default function NotifyModal({ variantId, productTitle, size, color, onClose }) {
  const { sessionToken } = useSession();
  const [email, setEmail] = useState('');
  const [state, setState] = useState({ loading: false, error: '', success: '' });

  async function handleSubmit(e) {
    e.preventDefault();

    const emailError = validateStockAlertEmail(email);
    if (emailError) {
      setState({ loading: false, error: emailError, success: '' });
      return;
    }

    setState({ loading: true, error: '', success: '' });
    try {
      const response = await subscribeStockAlert(
        { variant: variantId, email },
        sessionToken
      );
      setState({
        loading: false,
        error: '',
        success:
          response.message || 'You will be notified when this variant is back in stock.'
      });
    } catch (err) {
      setState({
        loading: false,
        error: err.message || 'Unable to subscribe to restock alerts.',
        success: ''
      });
    }
  }

  return (
    <Modal title="Notify me when available" onClose={onClose}>
      <p>
        {productTitle} — {size} / {color} is out of stock.
      </p>

      {state.success && <div className="notice success">{state.success}</div>}
      {state.error && <div className="notice error">{state.error}</div>}

      {state.success ? (
        <div className="action-row">
          <button type="button" className="button secondary" onClick={onClose}>
            Close
          </button>
        </div>
      ) : (
        <form className="form-grid" onSubmit={handleSubmit}>
          <label>
            Email
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
            />
          </label>
          <div className="action-row">
            <button type="button" className="button secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" disabled={state.loading}>
              {state.loading ? 'Saving…' : 'Notify me'}
            </button>
          </div>
        </form>
      )}
    </Modal>
  );
}
