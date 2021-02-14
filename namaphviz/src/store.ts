import { configureStore, ThunkAction, Action } from '@reduxjs/toolkit';
import counterReducer from './features/counter/counterSlice';

import seekbarReducer from './features/seekbar/seekbarSlice'
import dataloaderReducer from './features/dataloader/dataloaderSlice';
import vizthemelistReducer from './features/vizthemelist/vizthemelistSlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    dataloader: dataloaderReducer,
    seekbar: seekbarReducer,
    vizthemelist: vizthemelistReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
