# AI-First CRM HCP Module

This repository contains the solution for **Task 1: AI-First CRM HCP Module**, an AI-driven Customer Relationship Management tool built for Life Science experts to manage Healthcare Professional (HCP) interactions.

## 🚀 Features & Architecture

The application offers field representatives the flexibility to log interactions with HCPs via a traditional structured form on the left or via a conversational **AI Assistant** on the right.

- **Frontend:** React, TypeScript, Vite, Tailwind CSS, Redux Toolkit, Google Inter Font.
- **Backend:** Python, FastAPI, SQLAlchemy.
- **Database:** PostgreSQL.
- **AI Agent Framework:** LangGraph.
- **LLM:** Groq API (`llama-3.3-70b-versatile` used as `gemma2-9b-it` has been decommissioned by Groq).

## 🧠 Role of the LangGraph AI Agent

The LangGraph Agent serves as the reasoning engine that manages HCP interaction data. Instead of forcing the user to manually click and type into form inputs, the user provides a natural language summary of their meeting to the chat interface. 

The LangGraph Agent receives this conversational context, extracts essential entities (HCP names, discussion points, action items), and invokes programmatic "Tools" to update the application form state directly. The agent acts seamlessly as a liaison between the user's natural language and the rigid database schema.

### Defined Tools

The LangGraph agent is equipped with the following 5 specific tools:

1. **`log_interaction`**
   - **Role:** Captures new interaction data from user descriptions. When a user says "I met with Dr. Smith and discussed Product X", this tool uses LLM intelligence to summarize the discussion, extract the HCP name, interaction type, and outcomes, and populate the draft log form.
2. **`edit_interaction`**
   - **Role:** Allows modification of currently logged data. If the user later types "Oh, please add that I sent him the Brochure," this tool safely merges the new information into the current form draft.
3. **`search_hcp_history`**
   - **Role:** Retrieves historical context from the CRM database. If a user asks "When did I last see Dr. Smith?", the agent queries past interaction logs to inform its response.
4. **`suggest_followups`**
   - **Role:** Analyzes the topics covered in the meeting and suggests proactive next steps to the rep (e.g., "Set up follow-up to review study data in 2 weeks").
5. **`lookup_materials`**
   - **Role:** Performs an inventory/database search for available marketing or educational materials so the agent can quickly provide product pamphlets or guides mentioned in the conversation.

## 🛠️ Instructions to Run Locally

### 1. Database Setup (PostgreSQL)
Ensure you have a PostgreSQL server running locally. Create a new database named `hcp_crm`.

### 2. Backend (FastAPI) Setup
```bash
cd hcp_crm/backend
# Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure your environment variables
# Open hcp_crm/backend/.env and set:
# GROQ_API_KEY="your_groq_api_key_here"
# DATABASE_URL="postgresql://username:password@localhost:5432/hcp_crm"

# Run the FastAPI server (runs on Port 8000)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend (React) Setup
Open a new terminal.
```bash
cd hcp_crm/frontend

# Install node dependencies
npm install

# Run the Vite Dev Server (runs on Port 5173)
npm run dev
```

Browse to `http://localhost:5173/` in your browser.
