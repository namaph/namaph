import React from 'react';
import DeckGL from '@deck.gl/react';
import {PolygonLayer} from '@deck.gl/layers';
import {GridLayer} from '@deck.gl/aggregation-layers';
import {StaticMap} from 'react-map-gl';
import config from '../../settings/.maptoken.json';
import gridData from '../../settings/sf-bike-parking.json';
import virtualData from '../../settings/product_io.json';
import bioDiv from '../../settings/biodiv.json';

const MAP_STYLE = 'mapbox://styles/ricky189/ckl2880100ncb17mlxy595yo4';
const MAPBOX_ACCESS_TOKEN = config.mapboxToken;

// Viewport settings

const colors = [[239,243,255],[198,219,239],[158,202,225],[107,174,214],[49,130,189],[8,81,156]];

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
  elevationRange: [0,100],
  elevationScale: 2,
  extruded: false,
  getPosition: d => d.COORDINATES as [number,number],
  opacity: 0.01,
  pickable: true,
});

const productIolayer = new PolygonLayer({
    id: 'polygon-layer',
    data: virtualData.GEOGRID.features,
    pickable: true,
    stroked: false,
    filled: true,
    wireframe: true,
    lineWidthMinPixels: 1,
    extruded: false,
    getPolygon: d => d.geometry.coordinates[0] as [number,number][],
    getElevation: d => 100,
    getFillColor: d => {
      return d.properties.color as [number,number,number];
    },
    getLineColor: [80, 80, 80],
    getLineWidth: 1,
    opacity: 0.1
});

const bioMasslayer = new PolygonLayer({
    id: 'polygon-layer',
    data: virtualData.GEOGRID.features,
    pickable: true,
    stroked: false,
    filled: true,
    wireframe: true,
    lineWidthMinPixels: 1,
    extruded: false,
    getPolygon: d => d.geometry.coordinates[0] as [number,number][],
    getElevation: d => bioDiv[d.properties.id].color*10,
    getFillColor: d => {
      return colors[bioDiv[d.properties.id].color] as [number,number,number];
    },
    getLineColor: [80, 80, 80],
    getLineWidth: 1,
    opacity: 0.2
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
      height="calc(100% - 40px)"
      layers={[bioMasslayer]}
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
