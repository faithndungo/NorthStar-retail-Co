import { useEffect, useMemo, useRef, useState } from 'react';
import { useSession } from '../../context/SessionContext.jsx';
import { getProducts, checkInventory } from '../../services/inventoryService.js';
import { normalizeStockStatus } from '../../utils/formatters.js';
import LoadingSkeleton from '../common/LoadingSkeleton.jsx';
import ErrorNotice from '../common/ErrorNotice.jsx';
import NotifyModal from './NotifyModal.jsx';

export default function StockChecker() {
  const { sessionToken } = useSession();

  // Catalog is OPTIONAL. If the backend exposes /inventory/products/ we use
  // dropdowns; otherwise we silently fall back to manual entry.
  const [products, setProducts] = useState([]);
  const [catalogAvailable, setCatalogAvailable] = useState(false);
  const [catalogLoading, setCatalogLoading] = useState(true);

  const [productId, setProductId] = useState('');
  const [size, setSize] = useState('');
  const [color, setColor] = useState('');

  const [stock, setStock] = useState(null);
  const [checking, setChecking] = useState(false);
  const [error, setError] = useState('');
  const [notifyOpen, setNotifyOpen] = useState(false);

  const dismissedRef = useRef('');
  const requestIdRef = useRef(0);

  const product = products.find((p) => String(p.id) === String(productId));

  const sizes = useMemo(
    () => (product ? [...new Set((product.variants || []).map((v) => v.size))] : []),
    [product]
  );
  const colors = useMemo(
    () => (product ? [...new Set((product.variants || []).map((v) => v.color))] : []),
    [product]
  );

  const selectedVariant = (product?.variants || []).find(
    (v) => v.size === size && v.color === color
  );

  const variantKey = `${productId}|${size}|${color}`;

  // 1. Try to load catalog — fail silently into manual mode (no error shown)
  useEffect(() => {
    let active = true;

    async function loadCatalog() {
      try {
        const list = await getProducts(sessionToken);
        if (active && list.length > 0) {
          setProducts(list);
          setCatalogAvailable(true);
        }
      } catch {
        // Catalog endpoint unavailable — manual entry mode is used instead.
        // Intentionally silent: this must not surface as a UI error.
      } finally {
        if (active) setCatalogLoading(false);
      }
    }

    loadCatalog();
    return () => {
      active = false;
    };
  }, [sessionToken]);

  useEffect(() => {
    dismissedRef.current = '';
  }, [variantKey]);

  // Reset variant fields only in catalog (dropdown) mode
  useEffect(() => {
    if (!catalogAvailable) return;
    setSize('');
    setColor('');
    setStock(null);
    setNotifyOpen(false);
    setError('');
  }, [productId, catalogAvailable]);

  async function runCheck() {
    if (!productId.trim() || !size.trim() || !color.trim()) return;

    const requestId = ++requestIdRef.current;
    setChecking(true);
    setError('');

    try {
      const result = await checkInventory(
        {
          product_id: productId.trim(),
          variant: selectedVariant?.id,
          size: size.trim(),
          color: color.trim()
        },
        sessionToken
      );

      if (requestId !== requestIdRef.current) return;

      const normalized = normalizeStockStatus(
        result.stock_status,
        result.available_count
      );

      setStock({ ...result, normalized });

      if (
        normalized.status === 'out_of_stock' &&
        dismissedRef.current !== variantKey
      ) {
        setNotifyOpen(true);
      } else if (normalized.status !== 'out_of_stock') {
        setNotifyOpen(false);
      }
    } catch (err) {
      if (requestId !== requestIdRef.current) return;
      setStock(null);
      setError(err.message || 'Unable to check stock.');
      setNotifyOpen(false);
    } finally {
      if (requestId === requestIdRef.current) setChecking(false);
    }
  }

  // 2. Catalog mode: auto-check as soon as a full variant is selected
  useEffect(() => {
    if (!catalogAvailable || !productId || !size || !color) return;
    const timer = setTimeout(runCheck, 250);
    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [catalogAvailable, productId, size, color, sessionToken]);

  // 3. Manual mode: explicit submit
  function handleSubmit(e) {
    e.preventDefault();
    runCheck();
  }

  function closeModal() {
    dismissedRef.current = variantKey;
    setNotifyOpen(false);
  }

  return (
    <section className="card" aria-label="Stock availability checker">
      <h2>Stock Availability</h2>
      <p>Check real-time stock across sizes and colors.</p>

      {catalogLoading ? (
        <LoadingSkeleton lines={3} />
      ) : (
        <form className="form-grid" onSubmit={handleSubmit}>
          {catalogAvailable ? (
            <>
              <label>
                Product
                <select
                  value={productId}
                  onChange={(e) => setProductId(e.target.value)}
                  required
                >
                  <option value="">Select a product</option>
                  {products.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.title}
                    </option>
                  ))}
                </select>
              </label>

              <label>
                Size
                <select
                  value={size}
                  onChange={(e) => setSize(e.target.value)}
                  disabled={!product}
                  required
                >
                  <option value="">Select size</option>
                  {sizes.map((s) => (
                    <option key={s} value={s}>
                      {s}
                    </option>
                  ))}
                </select>
              </label>

              <label>
                Color
                <select
                  value={color}
                  onChange={(e) => setColor(e.target.value)}
                  disabled={!product}
                  required
                >
                  <option value="">Select color</option>
                  {colors.map((c) => (
                    <option key={c} value={c}>
                      {c}
                    </option>
                  ))}
                </select>
              </label>
            </>
          ) : (
            <>
              <label>
                Product ID or SKU
                <input
                  value={productId}
                  onChange={(e) => setProductId(e.target.value)}
                  placeholder="e.g. 1 or NS-JKT-001"
                  required
                />
              </label>

              <label>
                Size
                <input
                  value={size}
                  onChange={(e) => setSize(e.target.value)}
                  placeholder="e.g. M"
                  required
                />
              </label>

              <label>
                Color
                <input
                  value={color}
                  onChange={(e) => setColor(e.target.value)}
                  placeholder="e.g. Black"
                  required
                />
              </label>

              <button
                type="submit"
                disabled={checking || !productId.trim() || !size.trim() || !color.trim()}
              >
                {checking ? 'Checking…' : 'Check stock'}
              </button>
            </>
          )}
        </form>
      )}

      {checking && <LoadingSkeleton lines={2} />}
      <ErrorNotice message={error} />

      {stock && !checking && (
        <div className="stock-result">
          <span className={`badge ${stock.normalized.className}`}>
            {stock.normalized.label}
          </span>
          {stock.normalized.status !== 'out_of_stock' && (
            <span className="muted">
              Available count: {stock.available_count}
            </span>
          )}
        </div>
      )}

      {stock?.normalized?.status === 'out_of_stock' && !notifyOpen && (
        <div className="action-row">
          <button type="button" onClick={() => setNotifyOpen(true)}>
            Notify me when available
          </button>
        </div>
      )}

      {notifyOpen && (
        <NotifyModal
          variantId={selectedVariant?.id || stock?.variant_id || stock?.variant}
          productTitle={product?.title || productId}
          size={size}
          color={color}
          onClose={closeModal}
        />
      )}
    </section>
  );
}