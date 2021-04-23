import React, { useContext, useEffect } from 'react';
import './Header.css';

const Header = () => {
  return (
    <nav className="navbar bg-primary-color">
      <a className="navbar-brand text-grey" href="#">
        G-Analysis
      </a>
      <div className="dropdown">
        <button className="btn-success btn dropdown-toggle" type="button" data-toggle="dropdown">
          Plots
        </button>
        <div className="dropdown-menu">
          <a href="#" className="dropdown-item">
            Cats
          </a>
        </div>
      </div>
    </nav>
  );
};

export default Header;
