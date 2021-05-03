import React, { useState, useEffect } from 'react';
import './IMap.css';

const IMap = prop => {
  const { zoom, mapname, url, title, selcoordinates } = prop;
  const [map, setMap] = useState(null);
  const [markers, setMarkers] = useState([]);

  useEffect(() => {
    var map = L.map(mapname).setView([0.5, 0.5], zoom);
    L.tileLayer(url, {
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);
    setMap(map);
  }, []);

  useEffect(() => {
    if (map != null) {
      var points = selcoordinates.split(';');
      var _markers = [];
      for (let i = 0; i < markers.length; i++) {
        map.removeLayer(markers[i]);
      }
      for (let i = 0; i < points.length; i++) {
        let point = points[i].split(',');
        console.log(point, mapname);
        if (mapname == point[0]) {
          let m = L.circle([point[1], point[2]], {
            color: 'red',
            fillColor: '#f03',
            opacity: 0.3,
            fillOpacity: 0.3,
            radius: 700,
          }).addTo(map);
          _markers.push(m);
        }
      }
      setMarkers(_markers);
    }
  }, [selcoordinates]);
  return (
    <div>
      <h5>{title}</h5>
      <div className="map__container" id={mapname}></div>
    </div>
  );
};

export default IMap;
