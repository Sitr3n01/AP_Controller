import { useState } from 'react';
import { PropertyProvider } from './contexts/PropertyContext';
import Sidebar from './components/Sidebar';
import ErrorBoundary from './components/ErrorBoundary';
import Dashboard from './pages/Dashboard';
import Calendar from './pages/Calendar';
import Conflicts from './pages/Conflicts';
import Statistics from './pages/Statistics';
import Documents from './pages/Documents';
import Emails from './pages/Emails';
import Notifications from './pages/Notifications';
import Settings from './pages/Settings';
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />;
      case 'calendar':
        return <Calendar />;
      case 'conflicts':
        return <Conflicts />;
      case 'statistics':
        return <Statistics />;
      case 'documents':
        return <Documents />;
      case 'emails':
        return <Emails />;
      case 'notifications':
        return <Notifications />;
      case 'settings':
        return <Settings />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <PropertyProvider>
      <div className="app">
        <Sidebar
          currentPage={currentPage}
          onPageChange={setCurrentPage}
          collapsed={sidebarCollapsed}
          onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
        />
        <main className={`main-content ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
          <ErrorBoundary key={currentPage}>
            {renderPage()}
          </ErrorBoundary>
        </main>
      </div>
    </PropertyProvider>
  );
}

export default App;
