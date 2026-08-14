import { useSession } from '../../context/SessionContext.jsx';

const ACTIONS = [
  { key: 'home', label: 'Home' },
  { key: 'order', label: 'Track Order' },
  { key: 'return', label: 'Start Return' },
  { key: 'stock', label: 'Stock Check' }
];

export default function HeaderBar({ active, onNavigate }) {
  const { sessionToken, sessionLoading, sessionWarning } = useSession();

  return (
    <header className="app-header">
      <div className="brand">
        <h1>Northstar Support Deflection MVP</h1>
        <p>Guest self-service for order, return, and stock questions.</p>
      </div>

      <nav className="nav-actions" aria-label="Support actions">
        {ACTIONS.map((a) => (
          <button
            key={a.key}
            type="button"
            className={active === a.key ? 'active' : ''}
            onClick={() => onNavigate(a.key)}
          >
            {a.label}
          </button>
        ))}
      </nav>

      <div className="session-status" title={sessionWarning}>
        {sessionLoading
          ? 'Starting guest session…'
          : sessionToken
            ? 'Guest session active'
            : 'Guest session unavailable'}
      </div>
    </header>
  );
}