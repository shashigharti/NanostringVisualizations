import React, { useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'jquery/dist/jquery.min.js';
import 'bootstrap/dist/js/bootstrap.min.js';
import './App.css';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { Dashboard, Header } from './packages/Core';

const App = () => {
  return (
    <>
      <Router basename={process.env.SUB_URL}>
        <Header />
        <Route path="/" component={Dashboard} />
      </Router>
    </>
  );
};

export default App;
