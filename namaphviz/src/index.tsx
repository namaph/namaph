import React from 'react';
import ReactDOM from 'react-dom';
import { useSelector } from "react-redux";

import './index.css';
// import App from './app/App';
import {Vizthemelist} from "./features/vizthemelist/Vizthemelist"
import {Indicatorlist} from './features/indicatorlist/Indicatorlist'
import {Mapcontroller} from './features/mapcontroller/Mapcontroller'
import {Seekbar} from './features/seekbar/Seekbar'
import {DeckMap} from './features/deckgl/Deckgl'

import DataLoader from './features/dataloader/DataLoader'
import {selectReady} from './features/dataloader/dataloaderSlice'

import { store } from './store';
import { Provider } from 'react-redux';
import * as serviceWorker from './serviceWorker';

// import ParentSize from '@visx/responsive/lib/components/ParentSize'

function App(props: any) {
  const ready = useSelector(selectReady);
  const { tableName } = props;

  return (
      <>
        {
          !ready ? <DataLoader tableName={tableName} /> : (
            <>
              <DeckMap />
              <Vizthemelist />
              <Indicatorlist />
              <Mapcontroller />
              <Seekbar />
            </>
        )}
      </>
  );
}

ReactDOM.render(
  <React.StrictMode>  
    <Provider store={store}>  
      <App tableName="roppongi" />
    </Provider>  
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.register();
