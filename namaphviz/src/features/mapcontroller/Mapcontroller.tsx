import styles from "./Mapcontroller.module.css"
import Icon from './namaph_mini_1.svg'
import React from "react"

export function Mapcontroller () {
    return (
        <div className={styles.maphoge} >
            <img src={Icon} className={styles.maplogo}  />
        </div>
    )
}
