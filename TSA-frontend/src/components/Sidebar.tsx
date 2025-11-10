import { useState } from 'react';

interface SidebarProps {
  currentView: string;
  onViewChange: (view: string) => void;
  user?: string;
}

export default function Sidebar({ currentView, onViewChange, user = "member@mail.com" }: SidebarProps) {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard'},
    { id: 'tasks', label: 'Tasks'},
  ];

  return (
    <div className="sidebar sidebar-open">
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <span className="logo-text">TSA Portal</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <button
            key={item.id}
            className={`nav-item ${currentView === item.id ? 'nav-item-active' : ''}`}
            onClick={() => onViewChange(item.id)}
          >
            <span className="nav-label">{item.label}</span>
          </button>
        ))}
      </nav>

    </div>
  );
}