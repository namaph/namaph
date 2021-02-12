import React from 'react';
import DeckGL from '@deck.gl/react';
import {PolygonLayer} from '@deck.gl/layers';
import {GridLayer} from '@deck.gl/aggregation-layers';
import {StaticMap} from 'react-map-gl';
import config from '../../settings/.maptoken.json';
import gridData from '../../settings/sf-bike-parking.json';
import virtualData from '../../settings/roppongi_virtual.json';

const MAP_STYLE = 'mapbox://styles/mapbox/dark-v10';
const MAPBOX_ACCESS_TOKEN = config.mapboxToken;

// Viewport settings
const INITIAL_VIEW_STATE = {
  longitude: 139.7315,
  latitude: 35.6556,
  zoom: 15,
  pitch: 0,
  bearing: 0
};

const gridlayer = new GridLayer({
  id: 'GridLayer',
  data: gridData,

  /* props from GridLayer class */

  cellSize: 200,
  colorRange: [[255, 255, 178], [254, 217, 118], [254, 178, 76], [253, 141, 60], [240, 59, 32], [189, 0, 38]],
  elevationRange: [0,100],
  elevationScale: 2,
  extruded: false,
  getPosition: d => d.COORDINATES as [number,number],
  opacity: 0.01,
  pickable: true,

});

const polygonlayer = new PolygonLayer({
    id: 'polygon-layer',
    data: virtualData.GEOGRID.features,
    pickable: true,
    stroked: false,
    filled: true,
    wireframe: true,
    lineWidthMinPixels: 1,
    getPolygon: d => d.geometry.coordinates[0] as [number,number][],
    getElevation: d => 100,
    getFillColor: d => d.properties.color as [number,number,number],
    getLineColor: [80, 80, 80],
    getLineWidth: 1,
    opacity: 0.05
});

// Data to be used by the LineLayer

// DeckGL react component
export function DeckMap() {


  return (
    <DeckGL
      initialViewState={INITIAL_VIEW_STATE}
      controller={true}
      effects={[]}
      width="100%"
      height="100%"
      layers={[polygonlayer]}
    >
      <StaticMap
        width="100%"
        height="100%"
        mapboxApiAccessToken={MAPBOX_ACCESS_TOKEN}
        mapStyle={MAP_STYLE}
      />
    </DeckGL>
  );
}
