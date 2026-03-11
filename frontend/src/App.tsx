import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import type { RootState, AppDispatch } from './store';
import { updateField } from './store/formSlice';
import { sendMessageToAgent } from './store/chatSlice';
import { FaMicrophone, FaPaperPlane } from 'react-icons/fa';

function App() {
  const dispatch = useDispatch<AppDispatch>();

  // Redux state
  const form = useSelector((state: RootState) => state.form);
  const chat = useSelector((state: RootState) => state.chat);

  // Local state for chat input
  const [chatInput, setChatInput] = useState('');

  // Form handlers
  const handleFormChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    dispatch(updateField({ field: e.target.name as any, value: e.target.value }));
  };

  // Chat handlers
  const handleSendMessage = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!chatInput.trim() || chat.isLoading) return;
    dispatch(sendMessageToAgent(chatInput));
    setChatInput('');
  };

  return (
    <div className="flex h-screen w-full bg-[#f4f6f8] text-[#333] font-sans">

      {/* LEFT PANEL: STRUCTURED FORM */}
      <div className="flex-1 overflow-y-auto p-6 border-r border-gray-200 bg-white">
        <h1 className="text-2xl font-bold mb-6 text-gray-800">Log HCP Interaction</h1>

        <div className="bg-white border rounded-lg shadow-sm">
          <div className="bg-gray-50 px-4 py-3 border-b font-semibold text-gray-700">Interaction Details</div>

          <div className="p-4 space-y-5">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-gray-600 mb-1">HCP Name</label>
                <input
                  type="text" name="hcp_name" value={form.hcp_name} onChange={handleFormChange}
                  className="w-full border rounded-md p-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                  placeholder="Search or select HCP..."
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-gray-600 mb-1">Interaction Type</label>
                <select
                  name="interaction_type" value={form.interaction_type} onChange={handleFormChange}
                  className="w-full border rounded-md p-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                >
                  <option>Meeting</option>
                  <option>Call</option>
                  <option>Email</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-gray-600 mb-1">Date</label>
                <input
                  type="date" name="date" value={form.date} onChange={handleFormChange}
                  className="w-full border rounded-md p-2 text-sm"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-gray-600 mb-1">Time</label>
                <input
                  type="time" name="time" value={form.time} onChange={handleFormChange}
                  className="w-full border rounded-md p-2 text-sm"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-600 mb-1">Attendees</label>
              <input
                type="text" name="attendees" value={form.attendees} onChange={handleFormChange}
                className="w-full border rounded-md p-2 text-sm"
                placeholder="Enter names or search..."
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-600 mb-1">Topics Discussed</label>
              <div className="relative">
                <textarea
                  name="topics_discussed" value={form.topics_discussed} onChange={handleFormChange}
                  className="w-full border rounded-md p-2 text-sm h-24 resize-none"
                  placeholder="Enter key discussion points..."
                ></textarea>
                <button className="absolute bottom-2 right-2 text-gray-400 hover:text-gray-600">
                  <FaMicrophone />
                </button>
              </div>
              <button className="mt-2 text-xs text-blue-600 bg-blue-50 px-3 py-1.5 rounded flex items-center gap-2 hover:bg-blue-100">
                <FaMicrophone /> Summarize from Voice Note (Requires Consent)
              </button>
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-600 mb-1">Outcomes</label>
              <textarea
                name="outcomes" value={form.outcomes} onChange={handleFormChange}
                className="w-full border rounded-md p-2 text-sm h-20 resize-none"
                placeholder="Key outcomes or agreements..."
              ></textarea>
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-600 mb-1">Follow-up Actions</label>
              <textarea
                name="follow_up_actions" value={form.follow_up_actions} onChange={handleFormChange}
                className="w-full border rounded-md p-2 text-sm h-20 resize-none"
                placeholder="Enter next steps or tasks..."
              ></textarea>
            </div>

          </div>
        </div>
      </div>

      {/* RIGHT PANEL: AI ASSISTANT CHAT */}
      <div className="w-[400px] flex flex-col bg-gray-50 relative">
        <div className="p-4 border-b bg-white flex items-center gap-2 shadow-sm z-10">
          <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold text-sm">
            AI
          </div>
          <h2 className="font-semibold text-gray-800 text-sm">AI Assistant<br /><span className="text-xs font-normal text-gray-500">Log interaction via chat</span></h2>
        </div>

        <div className="flex-1 p-4 overflow-y-auto space-y-4">
          {chat.messages.map((msg) => (
            <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div
                className={`max-w-[85%] rounded-2xl p-3 text-sm shadow-sm ${msg.sender === 'user'
                  ? 'bg-blue-600 text-white rounded-tr-none'
                  : 'bg-white text-gray-800 border rounded-tl-none'
                  }`}
              >
                {msg.text}
              </div>
            </div>
          ))}
          {chat.isLoading && (
            <div className="flex justify-start">
              <div className="bg-white text-gray-500 border rounded-2xl rounded-tl-none p-3 text-sm flex gap-1">
                <span className="animate-bounce">.</span><span className="animate-bounce delay-100">.</span><span className="animate-bounce delay-200">.</span>
              </div>
            </div>
          )}
        </div>

        <div className="p-4 bg-white border-t">
          <form className="flex gap-2" onSubmit={handleSendMessage}>
            <input
              type="text"
              value={chatInput}
              onChange={e => setChatInput(e.target.value)}
              placeholder="Describe interaction..."
              className="flex-1 border rounded-lg px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-blue-500"
              disabled={chat.isLoading}
            />
            <button
              type="submit"
              className={`bg-gray-800 text-white px-4 py-2 rounded-lg text-sm flex items-center gap-2 hover:bg-gray-700 transition ${chat.isLoading ? 'opacity-50' : ''}`}
              disabled={chat.isLoading}
            >
              <FaPaperPlane /> Log
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;
