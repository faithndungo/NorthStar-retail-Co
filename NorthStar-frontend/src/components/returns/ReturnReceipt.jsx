import FakeQr from './FakeQr.jsx';
import { RETURN_REASONS } from '../../utils/constants.js';

export default function ReturnReceipt({ returnData, orderNumber, reason, onReset }) {
  const returnId = returnData?.id || returnData?.return_id || `return-${orderNumber}`;
  const labelUrl =
    returnData?.shipping_label_url ||
    returnData?.label_url ||
    '';
  const qrValue = returnData?.qr_code_value || `northstar-return:${returnId}:order:${orderNumber}`;
  const reasonLabel = RETURN_REASONS.find((r) => r.value === reason)?.label || reason;

  return (
    <div className="receipt">
      <h3>Return confirmation</h3>

      <dl className="result-meta">
        <div><dt>Return ID</dt><dd>{returnId}</dd></div>
        <div><dt>Order</dt><dd>{orderNumber}</dd></div>
        <div><dt>Status</dt><dd>{returnData?.status || 'submitted'}</dd></div>
        {reasonLabel && <div><dt>Reason</dt><dd>{reasonLabel}</dd></div>}
      </dl>

      <FakeQr value={qrValue} />

      {labelUrl ? (
        <a className="button" href={labelUrl} download="northstar-return-label.txt">
          Download shipping label
        </a>
      ) : (
        <p className="notice">Label will be available once the return is approved.</p>
      )}

      <div className="action-row">
        <button type="button" className="button secondary" onClick={() => window.print()}>
          Print receipt
        </button>
        <button type="button" className="button secondary" onClick={onReset}>
          Start another return
        </button>
      </div>
    </div>
  );
}