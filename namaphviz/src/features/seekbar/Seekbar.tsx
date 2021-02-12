import React from 'react'
import styles from './Seekbar.module.css';

import Typography from '@material-ui/core/Typography'
import Slider from '@material-ui/core/Slider'
import { withStyles, makeStyles } from '@material-ui/core/styles';
import config from '../../settings/config.json';

const seekconf = config.seekConf;

const PrettoSlider = withStyles({
  root: {
    color: '#5DB6E8',
    height: 4,
    marginTop:4,
    marginLeft:100,
    width:'calc(100% - 200px)'
  },
  thumb: {
    height: 16,
    width: 16,
    backgroundColor: '#fff',
    border: '2px solid #CCC',
    marginTop: -6,
    marginLeft: -8,
    '&:focus, &:hover, &$active': {
      boxShadow: 'inherit',
    },
  },
  active: {},
  valueLabel: {
    left: 'calc(-50% - 4px)',
    color: '#000',
  },
  track: {
    height: 4,
    borderRadius: 2,
  },
  rail: {
    height: 4,
    borderRadius: 2,
  },
  mark: {
    backgroundColor: '#fff',
    height: 8,
    width: 2,
    marginTop: -3,
  },
})(Slider);

export function Seekbar() {
    return (
        <div className={styles.seekhoge} >
        <span className={styles.yearstart}>{seekconf.valueMin}</span>
        <span className={styles.yearend}>{seekconf.valueMax}</span>
            <PrettoSlider
                defaultValue={seekconf.defaultValue}
                aria-labelledby="discrete-slider-small-steps"
                step={1}
                marks
                min={seekconf.valueMin}
                max={seekconf.valueMax}
                valueLabelDisplay="auto"
            />
        </div>
    )
}
