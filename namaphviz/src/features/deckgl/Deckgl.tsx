import React from 'react';
import { useEffect} from 'react';
import DeckGL from '@deck.gl/react';
import {PolygonLayer} from '@deck.gl/layers';
import {GridLayer} from '@deck.gl/aggregation-layers';
import {StaticMap} from 'react-map-gl';
import config from '../../settings/.maptoken.json';
import gridData from '../../settings/sf-bike-parking.json';

import { useSelector } from "react-redux";
import { selectindex } from "../vizthemelist/vizthemelistSlice"
import { selectYear} from "../seekbar/seekbarSlice"

import geomap from '../../settings/0/heatmap.json'
import biodiv from '../../settings/1/heatmap.json'
import biomass from '../../settings/2/heatmap.json'
import pathogen from '../../settings/3/biodiv.json'

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

const Maplayer = (i:any) => new PolygonLayer({
    id: 'polygon-layer',
    data: geomap,
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

const bioMasslayer = (i: any) =>  new PolygonLayer({
  id: 'polygon-layer',
  data: geomap,
  pickable: true,
  stroked: false,
  filled: true,
  wireframe: true,
  lineWidthMinPixels: 1,
  extruded: false,
  getPolygon: d => d.geometry.coordinates[0] as [number,number][],
  getElevation: d => biomass[i][d.properties.id].color*10,
  getFillColor: d => {
    return colors[biomass[i][d.properties.id].color] as [number,number,number];
  },
  getLineColor: [80, 80, 80],
  getLineWidth: 1,
  opacity: 0.2
});

const bioDivlayer = (i:any) => new PolygonLayer({
    id: 'polygon-layer',
    data: geomap,
    pickable: true,
    stroked: false,
    filled: true,
    wireframe: true,
    lineWidthMinPixels: 1,
    extruded: false,
    getPolygon: d => d.geometry.coordinates[0] as [number,number][],
    getElevation: d => biodiv[i][d.properties.id].color*10,
    getFillColor: d => {
      return colors[biodiv[i][d.properties.id].color] as [number,number,number];
    },
    getLineColor: [80, 80, 80],
    getLineWidth: 1,
    opacity: 0.2
});

const pathogenlayer = (i:any) => new PolygonLayer({
  id: 'polygon-layer',
  data: geomap,
  pickable: true,
  stroked: false,
  filled: true,
  wireframe: true,
  lineWidthMinPixels: 1,
  extruded: false,
  getPolygon: d => d.geometry.coordinates[0] as [number,number][],
  getElevation: d => pathogen[d.properties.id].color*10,
  getFillColor: d => {
    return colors[pathogen[d.properties.id].color] as [number,number,number];
  },
  getLineColor: [80, 80, 80],
  getLineWidth: 1,
  opacity: 0.2
});

// Data to be used by the LineLayer

// DeckGL react component
export function DeckMap() {
  var idx = useSelector(selectindex);
  var year = useSelector(selectYear)
  const themelist = [Maplayer, bioDivlayer, bioMasslayer, pathogenlayer]

  var layer = [Maplayer(0)]

  useEffect(
    () => {
        deck.setProps({layer: themelist[idx](Number(year)-2045}));
        console.log(layer)
    },
    [ idx, year ]
  );
  
  function render (idx:any, year:any) {
    return (
      <>
        <DeckGL
          initialViewState={INITIAL_VIEW_STATE}
          controller={true}
          effects={[]}
          width="100%"
          height="calc(100% - 40px)"
          layers={[themelist[idx](year)]}
          debug={true}
        >
          <StaticMap
            width="100%"
            height="100%"
            mapboxApiAccessToken={MAPBOX_ACCESS_TOKEN}
            mapStyle={MAP_STYLE}
          />
        </DeckGL>
        </>
    );
  }
  return render(idx, year)
}
