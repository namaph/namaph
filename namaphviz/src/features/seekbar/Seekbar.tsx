import React from 'react'
import styles from './Seekbar.module.css';

import Typography from '@material-ui/core/Typography'
import Slider from '@material-ui/core/Slider'

export function Seekbar() {
    return (
        <div className={styles.seekhoge} >
            <Typography id="discrete-slider-small-steps" gutterBottom>
                Small steps
            </Typography>
            <Slider
                defaultValue={0.00000005}
                aria-labelledby="discrete-slider-small-steps"
                step={0.00000001}
                marks
                min={-0.00000005}
                max={0.0000001}
                valueLabelDisplay="auto"
            />
        </div>
    )
}