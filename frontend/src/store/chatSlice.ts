import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import axios from 'axios';
import { updateFromAI } from './formSlice';

export interface ChatMessage {
    id: string;
    text: string;
    sender: 'user' | 'agent';
}

interface ChatState {
    messages: ChatMessage[];
    isLoading: boolean;
    interactionId: number | null;
}

const initialState: ChatState = {
    messages: [
        {
            id: '1',
            text: 'Hello! I am your AI Assistant. You can tell me about your interaction, and I will handle filling out the log for you.',
            sender: 'agent'
        }
    ],
    isLoading: false,
    interactionId: null
};

// Async thunk to send message to backend and parse response
export const sendMessageToAgent = createAsyncThunk(
    'chat/sendMessage',
    async (text: string, { dispatch, getState }) => {
        // Add user message immediately
        const userMsg: ChatMessage = { id: Date.now().toString(), text, sender: 'user' };
        dispatch(addMessage(userMsg));

        const state: any = getState();
        const interactionId = state.chat.interactionId;

        try {
            const response = await axios.post('http://localhost:8000/chat', {
                message: text,
                interaction_id: interactionId
            });

            const { chat_response, form_updates } = response.data;

            // Update form if AI updated it via LangGraph tools
            if (form_updates && Object.keys(form_updates).length > 0) {
                // filter out nulls
                const cleanUpdates = Object.fromEntries(
                    Object.entries(form_updates).filter(([_, v]) => v != null)
                );
                dispatch(updateFromAI(cleanUpdates));
            }

            // Return text to add to chat history
            return chat_response;
        } catch (error) {
            console.error(error);
            return "Sorry, I encountered an error communicating with the server.";
        }
    }
);

const chatSlice = createSlice({
    name: 'chat',
    initialState,
    reducers: {
        addMessage: (state, action: PayloadAction<ChatMessage>) => {
            state.messages.push(action.payload);
        },
        clearChat: () => initialState
    },
    extraReducers: (builder) => {
        builder
            .addCase(sendMessageToAgent.pending, (state) => {
                state.isLoading = true;
            })
            .addCase(sendMessageToAgent.fulfilled, (state, action) => {
                state.isLoading = false;
                state.messages.push({
                    id: Date.now().toString(),
                    text: action.payload,
                    sender: 'agent'
                });
            })
            .addCase(sendMessageToAgent.rejected, (state, action) => {
                state.isLoading = false;
                state.messages.push({
                    id: Date.now().toString(),
                    text: "Agent error: failed to fetch.",
                    sender: 'agent'
                });
            });
    }
});

export const { addMessage, clearChat } = chatSlice.actions;
export default chatSlice.reducer;
