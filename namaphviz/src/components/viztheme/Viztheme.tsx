import React from 'react';
import styles from './Viztheme.module.css';
import styled from 'styled-components';



const Selector = styled.div`
  width: 50px;
  height: 50px;
  margin-left:15px;
  background-color: #222;
  border-radius: 6px;
  border: 2px #999 solid;
  transition: border 0.2s ease;
  box-sizing: border-box;
  cursor:pointer;
  &:hover {

  }
`;

const Input = styled.input`
  display: none;
  &:checked + label > ${Selector} {
    border: 2px #FFF solid;
  }
`;


export function Viztheme (props: any) {
    return (
        <div className={styles.hogepiyo} >
            <Input type="radio" name={props.name} value={props.value} id={props.ioname} />
            <label htmlFor={props.ioname}><Selector /><span className={styles.themelabel}>{props.value}</span></label>
        </div>
    );
}
