import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { RootState } from '../../store';

interface IndicatorList {
  currentidx: number
}

const initialState: IndicatorList = {
  currentidx: 0
};

export const vizthemelistSlice = createSlice({
  name: 'dataloader',
  initialState: initialState,
  reducers: {
    setIndex: (state, action: PayloadAction<number>) => {
      state.currentidx = action.payload;
    },
  }
})


export const { setIndex} = vizthemelistSlice.actions;

export const selectReady = (state: RootState) => state.dataloader.ready;
export default vizthemelistSlice.reducer;