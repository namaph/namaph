
import React from 'react';
import { LineChart, Line, XAxis, YAxis } from 'recharts';

import config from '../../settings/config.json';
import styles from './Indicatorlist.module.css';
import totalBiomass from '../../settings/total_biomass.json';

const data = [
  {
    name: 'Page A',
    uv: 4000,
    pv: 2400,
    amt: 2400,
  },
  {
    name: 'Page B',
    uv: 3000,
    pv: 1398,
    amt: 2210,
  },
  {
    name: 'Page C',
    uv: 2000,
    pv: 9800,
    amt: 2290,
  },
  {
    name: 'Page D',
    uv: 2780,
    pv: 3908,
    amt: 2000,
  },
  {
    name: 'Page E',
    uv: 1890,
    pv: 4800,
    amt: 2181,
  },
  {
    name: 'Page F',
    uv: 2390,
    pv: 3800,
    amt: 2500,
  },
  {
    name: 'Page G',
    uv: 3490,
    pv: 4300,
    amt: 2100,
  },
];


export function Indicatorlist() {
    const modlist = config.modules[0].indicators
    return (
        <div className={styles.indhoge}>
          <span className={styles.graphtitle}>Total Biomass</span>
          <div className={styles.insideBack}>
          <LineChart width={300} height={150} data={totalBiomass} margin={{ top: 20, right: 20, left: 20, bottom: 20}}>
            <XAxis tick={{fontSize: 10}} height={10}dataKey="name"  />
            <YAxis tick={{fontSize: 10}} width={40} />
            <Line type="monotone" dataKey="total_biomass" stroke="#5DB6E8" />
          </LineChart>
          </div>

          <span className={styles.graphtitle}>Graph 2</span>
          <div className={styles.insideBack}>
          <LineChart width={300} height={150} data={data} margin={{ top: 20, right: 20, left: 20, bottom: 20}}>
            <XAxis tick={{fontSize: 10}} height={10}dataKey="name"  />
            <YAxis tick={{fontSize: 10}} width={20} />
            <Line type="monotone" dataKey="uv" stroke="#5DB6E8" />
          </LineChart>
          </div>
        </div>
    )
}
