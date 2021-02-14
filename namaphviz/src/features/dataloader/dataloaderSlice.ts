import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { AppThunk, RootState } from '../../store';

interface DataLoaderState {
  ready: boolean;
  geogrid: Array<any>;
  module: object;
}

const initialState: DataLoaderState = {
  ready: false,
  geogrid: [],
  module: {},
};

export const dataloaderSlice = createSlice({
  name: 'dataloader',
  initialState: initialState,
  reducers: {
    setReadyState: (state, action: PayloadAction<boolean>) => {
      state.ready = action.payload;
    },
    setGeogrid: (state, action: PayloadAction<Array<any>>) => {
      state.geogrid = action.payload;
    },
    setModule: (state, action: PayloadAction<any>) => {
      let mod: Object = action.payload;
      state.module = mod;
    }
  }
})


export const { setReadyState, setGeogrid, setModule } = dataloaderSlice.actions;

export const selectReady = (state: RootState) => state.dataloader.ready;
export default dataloaderSlice.reducer;