import React from 'react';
import './Header.css';

const Header = ({ title, user }) => {
  return (
    <header className="app-header">
      <div className="header-content">
        <h1 className="app-title">{title}</h1>
        <div className="user-info">
          <span>Welcome, {user?.name || 'Guest'}</span>
        </div>
      </div>
    </header>
  );
};

export default Header;
