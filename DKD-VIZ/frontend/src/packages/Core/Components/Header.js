import React, { useContext, useEffect } from 'react';
import './Header.css';

const Header = () => {
  return (
    <nav className="navbar bg-primary-color">
      <a className="navbar-brand text-grey" href="#">
        G-Analysis
      </a>
      <select>
        <option value="umap">UMap</option>
        <option value="heatmap">Heatmap</option>
      </select>
    </nav>
  );
};

export default Header;
