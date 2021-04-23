import React from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import './IMap.css';

const IMap = () => {
  const zoom = 11;
  return (
    <MapContainer className="map__container" center={[0.5, 0.5]} zoom={zoom}>
      <TileLayer
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url="http://localhost:5002/rgb/disease1B/scan/{z}/{x}/{y}.png?r=band2&g=band1&b=band0"
      />
    </MapContainer>
  );
};

export default IMap;
