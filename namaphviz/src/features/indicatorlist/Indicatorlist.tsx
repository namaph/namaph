
import React from 'react';
import { LineChart, Line, XAxis, YAxis, Legend, Tooltip } from 'recharts';

import config from '../../settings/config.json';
import styles from './Indicatorlist.module.css';
import y from '../../settings/150y.json';

import { useSelector } from "react-redux";
import { selectindex } from "../vizthemelist/vizthemelistSlice"

import norail from '../../settings/1/biomass.json'
import rail from '../../settings/2/biomass.json'
import orail from '../../settings/3/biomass.json'

import tnorail from '../../settings/1/biotrans.json'
import trail from '../../settings/2/biotrans.json'
import torail from '../../settings/3/biotrans.json'


function getColorArray(num: Number) {
  var result = [];
  for (var i = 0; i < num; i += 1) {
      var letters = '0123456789ABCDEF'.split('');
      var color = '#';
      for (var j = 0; j < 6; j += 1) {
          color += letters[Math.floor(Math.random() * 16)];
      }
      result.push(color);
  }
  return result;
}


export function Indicatorlist() {    
    const contents = [[[{}], norail, rail, orail], [[{}], tnorail, trail, torail]]

    let idx = useSelector(selectindex);

    let biotrans = Object.keys(contents[1][idx][0])
    let biocolor = getColorArray(100)
    console.log(biocolor)

    return (
        <div className={styles.indhoge}>
          <span className={styles.graphtitle}>Biomass</span>
          <div className={styles.insideBack}>
          <LineChart width={300} height={150} data={contents[0][idx]} margin={{ top: 20, right: 20, left: 20, bottom: 20}}>
            <XAxis tick={{fontSize: 10}} height={10} dataKey="name"  unit="年"/>
            <YAxis tick={{fontSize: 10}} width={40} unit="km" />
            <Line type="monotone" dataKey="biomass" stroke="#5DB6E8" dot={contents[0][idx].length < 20} />
          </LineChart>
          </div>

          <span className={styles.graphtitle}>Ecosystem Transition</span>
          <div className={styles.insideBack}>
          <LineChart width={300} height={150} data={contents[1][idx]} margin={{ top: 20, right: 20, left: 20, bottom: 20}}>
            <XAxis tick={{fontSize: 10}} height={10}dataKey="name"  />
            <YAxis tick={{fontSize: 10}} width={20} />
            { biotrans.map( k => <Line type="monotone" dot={false} dataKey={k} stroke={biocolor[Number(k.slice(2))]}/> )}
          </LineChart>
          </div>
        </div>
    )
}
