import { useEffect, useState } from 'react';
import { SessionProvider } from './context/SessionContext.jsx';
import HeaderBar from './components/layout/HeaderBar.jsx';
import Home from './pages/Home.jsx';
import Orders from './pages/Orders.jsx';
import Returns from './pages/Returns.jsx';
import Inventory from './pages/Inventory.jsx';

export default function App() {
  const routes = { '/': 'home', '/orders': 'order', '/returns': 'return', '/inventory': 'stock' };
  const paths = { home: '/', order: '/orders', return: '/returns', stock: '/inventory' };
  const [view, setView] = useState(() => routes[window.location.pathname] || 'home');

  useEffect(() => {
    function handlePopState() {
      setView(routes[window.location.pathname] || 'home');
    }
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  });

  function navigate(nextView) {
    const path = paths[nextView] || '/';
    if (window.location.pathname !== path) window.history.pushState({}, '', path);
    setView(nextView);
  }

  return (
    <SessionProvider>
      <div className="app">
        <HeaderBar active={view} onNavigate={navigate} />
        <main>
          {view === 'home' && <Home onNavigate={navigate} />}
          {view === 'order' && <Orders />}
          {view === 'return' && <Returns />}
          {view === 'stock' && <Inventory />}
        </main>
      </div>
    </SessionProvider>
  );
}
