export default function Home({ onNavigate }) {
  return (
    <section className="card">
      <h2>Welcome to Northstar Support</h2>
      <p>Choose an action below to get instant help without opening a ticket.</p>

      <div className="action-row">
        <button type="button" onClick={() => onNavigate('order')}>
          Track Order
        </button>
        <button type="button" onClick={() => onNavigate('return')}>
          Start Return
        </button>
        <button type="button" onClick={() => onNavigate('stock')}>
          Stock Check
        </button>
      </div>
    </section>
  );
}