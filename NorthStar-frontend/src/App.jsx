import { useState } from 'react';
import { SessionProvider } from './context/SessionContext.jsx';
import HeaderBar from './components/layout/HeaderBar.jsx';
import Home from './pages/Home.jsx';
import Orders from './pages/Orders.jsx';
import Returns from './pages/Returns.jsx';
import Inventory from './pages/Inventory.jsx';

export default function App() {
  const [view, setView] = useState('home');

  return (
    <SessionProvider>
      <div className="app">
        <HeaderBar active={view} onNavigate={setView} />
        <main>
          {view === 'home' && <Home onNavigate={setView} />}
          {view === 'order' && <Orders />}
          {view === 'return' && <Returns />}
          {view === 'stock' && <Inventory />}
        </main>
      </div>
    </SessionProvider>
  );
}