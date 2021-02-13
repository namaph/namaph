import React from 'react';
import styles from './Viztheme.module.css';
import styled from 'styled-components';
import iconBioMass from './namaph_icons_1.svg';
import iconBioDiv from './namaph_icons_2.svg';
import iconHumanHealth from './namaph_icons_3.svg';

import { useDispatch, useSelector } from "react-redux";
import { setIndex } from '../../features/vizthemelist/vizthemelistSlice'

const icons = [iconBioMass,iconBioDiv,iconHumanHealth];

const Selector = styled.div`
  position: relative;
  width: 50px;
  height: 50px;
  margin-left:15px;
  background-color: #f5f5f5;
  border-radius: 6px;
  border: 3px #fff solid;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
  box-sizing: border-box;
  cursor:pointer;
  &:hover {

  }
`;

const Icon = styled.img`
  position: absolute;
  width: 100%;
  opacity: 0.5;
  pointer-events: none;

`;

const Input = styled.input`
  display: none;
  &:checked + label > ${Selector} {
    background-color: #5DB6E8;
  }
  &:checked + label > ${Selector} > ${Icon} {
    filter: invert();
    opacity:1;
  }
`;




export function Viztheme (props: any) {
    let { idx } = props
    const dispatch = useDispatch();
    return (
        <div className={styles.hogepiyo} >
            <Input type="radio" name={props.name} value={props.value} id={props.ioname} onClick={(event) => dispatch(setIndex(idx))}/>
            <label htmlFor={props.ioname}><Selector><Icon src={icons[props.iconname]} /> </Selector><span className={styles.themelabel}>{props.value}</span></label>
        </div>
    );
}
