import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

export interface FormState {
  hcp_name: string;
  interaction_type: string;
  date: string;
  time: string;
  attendees: string;
  topics_discussed: string;
  materials: string[];
  outcomes: string;
  follow_up_actions: string;
}

const initialState: FormState = {
  hcp_name: '',
  interaction_type: 'Meeting',
  date: new Date().toISOString().split('T')[0],
  time: new Date().toTimeString().split(' ')[0].slice(0, 5),
  attendees: '',
  topics_discussed: '',
  materials: [],
  outcomes: '',
  follow_up_actions: ''
};

const formSlice = createSlice({
  name: 'form',
  initialState,
  reducers: {
    updateField: (state, action: PayloadAction<{ field: keyof FormState; value: any }>) => {
      // @ts-ignore
      state[action.payload.field] = action.payload.value;
    },
    updateFromAI: (state, action: PayloadAction<Partial<FormState>>) => {
      return { ...state, ...action.payload };
    },
    resetForm: () => initialState
  }
});

export const { updateField, updateFromAI, resetForm } = formSlice.actions;
export default formSlice.reducer;
