import React from 'react';
import { Viztheme } from '../../components/viztheme/Viztheme';

import config from '../../settings/config.json';
import styles from './Vizthemelist.module.css';

export function Vizthemelist() {
    const modlist = config.modules
    const value = "Vizthemelist"
    return (
        <div className={styles.vizhoge}>
            <form>
                {modlist.map(m => <Viztheme name={value} value={m.name}/>)}
            </form>
        </div>
    )
}