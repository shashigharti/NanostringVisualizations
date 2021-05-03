import React, { useState, useEffect } from 'react';
import IMap from './IMap';
import './Dashboard.css';
import Iframe from 'react-iframe';

const Dashboard = () => {
  const [selcoordinates, setSelcoordinates] = useState('');
  function initMessageHandler() {
    const messageHandler = event => {
      setSelcoordinates(event.data['selected_values'].join(';'));
    };
    window.addEventListener('message', messageHandler);
  }

  function handleChange(e) {
    setSelcoordinates(e.target.value);
  }

  return (
    <div className="container-fluid">
      <div className="marker__selcoordinates">
        <textarea
          type="text"
          id="selcoordinates"
          name="selcoordinates"
          value={selcoordinates}
          onChange={handleChange}
        />
      </div>
      <div className="row">
        <div className="col col-lg-5">
          <IMap
            title="DKD - disease1B"
            zoom="11"
            mapname="disease1B"
            url="rgb/disease1B/scan/{z}/{x}/{y}.png?r=band2&g=band1&b=band0"
            selcoordinates={selcoordinates}
          />
          <hr />
          <IMap
            title="DKD - disease2B"
            zoom="11"
            mapname="disease2B"
            url="rgb/disease2B/scan/{z}/{x}/{y}.png?r=band2&g=band1&b=band0"
            selcoordinates={selcoordinates}
          />
          <hr />
          <IMap
            title="normal - normal2B"
            zoom="11"
            mapname="normal2B"
            url="rgb/normal2B/scan/{z}/{x}/{y}.png?r=band2&g=band1&b=band0"
            selcoordinates={selcoordinates}
          />
        </div>
        <div className="col col-lg-7">
          {/* <Filter /> */}
          <h5>UMap</h5>
          <Iframe
            url="api/plots/umap"
            width="100%"
            height="100%"
            onLoad={initMessageHandler}
            className="myClassname"
            display="initial"
            position="relative"
          />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
