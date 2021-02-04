import React from 'react';
import styles from './Viztheme.module.css';

export function Viztheme (props: any) {
    return (
        <div className={styles.hogepiyo} >
            <input type="radio" name={props.name} value={props.value} />
            <label> {props.value} </label>
        </div>
    );
}