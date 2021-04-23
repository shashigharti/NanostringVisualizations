import React from 'react';
import './GTable.css';

const GTable = () => {
  return (
    <table className="table table-hover">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Gene Name</th>
          <th scope="col">disease3_scan | 001 | PanCK</th>
          <th scope="col">disease3_scan | 001 | neg</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">
            <input type="checkbox" className="form-check-input" id="exampleCheck1" />
          </th>
          <td>PADI2</td>
          <td>35</td>
          <td>36</td>
        </tr>
        <tr>
          <th scope="row">
            <input type="checkbox" className="form-check-input" id="exampleCheck1" />
          </th>
          <td>CYP24A1</td>
          <td>23</td>
          <td>32</td>
        </tr>
        <tr>
          <th scope="row">
            <input type="checkbox" className="form-check-input" id="exampleCheck1" />
          </th>
          <td>SUPT16H</td>
          <td>35</td>
          <td>66</td>
        </tr>
      </tbody>
    </table>
  );
};

export default GTable;
