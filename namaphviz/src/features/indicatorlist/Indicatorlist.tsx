import React from 'react';
import Example from '../../components/indicator/Example';

import config from '../../settings/config.json';
import styles from './Indicatorlist.module.css';

export function Indicatorlist() {
    const modlist = config.modules[0].indicators
    return (
        <div className={styles.indhoge}>
            <form>
                {modlist.map(m => <Example width={300} height={200}/>)}
            </form>
        </div>
    )
}