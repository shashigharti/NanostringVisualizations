import React, { useState, useEffect } from 'react';
import IMap from './IMap';
import './Dashboard.css';
import GTable from './GTable';
// import { embed } from '@bokeh/bokehjs/build/js/lib';
import Iframe from 'react-iframe';

const Dashboard = () => {
  useEffect(() => {
    // fetch('api/plots/volcano').then(function(response) {
    //   setPlot(response);
    // });
  }, []);
  // function setPlot(response) {
  //   embed.embed_item(response.data, 'volcano-plot');
  // }

  return (
    <div className="container-fluid">
      <div className="row">
        <div className="col col-lg-4">
          <IMap />
          <div className="card">
            <div className="card-body">
              <div className="row">
                <h5>
                  <b>File Name:</b>
                  Kidney_Raw_TargetCountMatrix
                </h5>
                <fieldset className="col col-lg-6">
                  <legend>Fields:</legend>
                  <ul class="list-group">
                    <li class="list-group-item">
                      &nbsp;
                      <input type="checkbox" className="form-check-input" id="exampleCheck1" />
                      &nbsp; Gene Name
                    </li>
                    <li class="list-group-item">
                      &nbsp;
                      <input type="checkbox" className="form-check-input" id="exampleCheck1" />
                      &nbsp; disease3_scan | 001 | PanCK
                    </li>
                    <li class="list-group-item">
                      &nbsp;
                      <input type="checkbox" className="form-check-input" id="exampleCheck1" />
                      &nbsp; disease3_scan | 001 | neg
                    </li>
                  </ul>
                </fieldset>
              </div>
              {/* <label class="form-label" for="customFile">
                Upload Data
              </label>
              <input type="file" class="form-control" id="customFile" /> */}
              <GTable />
            </div>
          </div>
          {/* <div className="g-table">
            <label class="form-label" for="customFile">
              Load Data
            </label>
            <input type="file" class="form-control" id="customFile" />
            <GTable />
          </div> */}
        </div>
        <div className="col col-lg-8">
          <div className="row">
            <div className="card col col-lg-6">
              <div className="card-body">
                <img
                  width="100%"
                  height="400px"
                  src="http://127.0.0.1:5000/api/plots/heatmap"
                  alt="viz"
                />
              </div>
            </div>
            <div className="card col col-lg-6">
              <div id="volcano-plot" className="card-body">
                <Iframe
                  url="http://127.0.0.1:5000/api/plots/volcano"
                  width="100%"
                  height="400px"
                  id="myId"
                  className="myClassname"
                  display="initial"
                  position="relative"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
