import { useSession } from '../../context/sessionContext.js';

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
        <button type="button" className="brand-link" onClick={() => onNavigate('home')}>
          <span className="brand-mark" aria-hidden="true">N</span>
          <span>
            <strong>NorthStar</strong>
            <small>Customer care</small>
          </span>
        </button>
      </div>

      <nav className="nav-actions" aria-label="Support actions">
        {ACTIONS.map((action) => (
          <button
            key={action.key}
            type="button"
            className={active === action.key ? 'active' : ''}
            onClick={() => onNavigate(action.key)}
          >
            {action.label}
          </button>
        ))}
      </nav>

      <div className="session-status" title={sessionWarning}>
        <span className={sessionToken ? 'status-dot active' : 'status-dot'} />
        {sessionLoading ? 'Connecting…' : sessionToken ? 'Secure session' : 'Offline mode'}
      </div>
    </header>
  );
}
