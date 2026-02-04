import { useState } from 'react';
import {
  Home,
  Calendar,
  AlertTriangle,
  Settings,
  ChevronLeft,
  ChevronRight,
  BarChart3
} from 'lucide-react';
import './Sidebar.css';

const Sidebar = ({ currentPage, onPageChange, collapsed, onToggleCollapse }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Home },
    { id: 'calendar', label: 'Calendário', icon: Calendar },
    { id: 'conflicts', label: 'Conflitos', icon: AlertTriangle },
    { id: 'statistics', label: 'Estatísticas', icon: BarChart3 },
    { id: 'settings', label: 'Configurações', icon: Settings },
  ];

  return (
    <div className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-header">
        <h1 className="sidebar-title">
          {!collapsed && 'SENTINEL'}
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
              {!collapsed && <span>{item.label}</span>}
            </button>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        {!collapsed && (
          <div className="sidebar-info">
            <p className="version">v1.0.0 - MVP1</p>
            <p className="status">
              <span className="status-dot"></span>
              Sistema Online
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;
