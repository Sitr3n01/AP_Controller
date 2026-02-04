import {
  Home,
  Calendar,
  AlertTriangle,
  Settings,
  ChevronLeft,
  ChevronRight,
  BarChart3,
  FileText,
  Mail,
  Bell
} from 'lucide-react';
import './Sidebar.css';

const Sidebar = ({ currentPage, onPageChange, collapsed, onToggleCollapse }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Home },
    { id: 'calendar', label: 'Calendario', icon: Calendar },
    { id: 'conflicts', label: 'Conflitos', icon: AlertTriangle },
    { id: 'statistics', label: 'Estatisticas', icon: BarChart3 },
    { id: 'documents', label: 'Documentos', icon: FileText },
    { id: 'emails', label: 'Emails', icon: Mail },
    { id: 'notifications', label: 'Notificacoes', icon: Bell },
    { id: 'settings', label: 'Configuracoes', icon: Settings },
  ];

  return (
    <div className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-header">
        <h1 className="sidebar-title">
          <span className="sidebar-title-text">LUMINA</span>
        </h1>
        <button
          className="collapse-btn"
          onClick={onToggleCollapse}
          title={collapsed ? 'Expandir' : 'Recolher'}
        >
          {collapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
        </button>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              className={`nav-item ${currentPage === item.id ? 'active' : ''}`}
              onClick={() => onPageChange(item.id)}
              title={collapsed ? item.label : ''}
            >
              <Icon size={20} />
              <span className="nav-label">{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-info">
          <p className="version">v2.2.0 - MVP2</p>
          <p className="status">
            <span className="status-dot"></span>
            <span className="status-text">Sistema Online</span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
