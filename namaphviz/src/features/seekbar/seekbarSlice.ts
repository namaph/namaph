import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { AppThunk, RootState } from '../../store';

interface DataLoaderState {
  year: number | number[]
}

const initialState: DataLoaderState = {
  year: 2045
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