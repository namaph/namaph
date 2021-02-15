import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { RootState } from '../../store';
import config from '../../settings/config.json';

interface DataLoaderState {
  year: number | number[]
}

const seekconf = config.seekConf;


const initialState: DataLoaderState = {
  year: seekconf.valueMin
};

export const dataloaderSlice = createSlice({
  name: 'dataloader',
  initialState: initialState,
  reducers: {
    setYear: (state, action:PayloadAction<number | number[]>) => {
        state.year = action.payload;
    }
  }
})


export const { setYear } = dataloaderSlice.actions;

export const selectYear = (state: RootState) => state.seekbar.year;
export default dataloaderSlice.reducer;