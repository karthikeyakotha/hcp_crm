from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from dotenv import load_dotenv
load_dotenv()

from . import models, schemas, agent
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-First CRM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-First CRM API"}

# Basic CRUD for Demo
@app.get("/hcps", response_model=List[schemas.HCPOut])
def get_hcps(db: Session = Depends(get_db)):
    return db.query(models.HCP).all()

@app.post("/interactions", response_model=schemas.InteractionOut)
def create_interaction(data: schemas.InteractionCreate, db: Session = Depends(get_db)):
    hcp = db.query(models.HCP).filter(models.HCP.name == data.hcp_name).first()
    if not hcp:
        hcp = models.HCP(name=data.hcp_name)
        db.add(hcp)
        db.commit()
        db.refresh(hcp)
    
    interaction = models.Interaction(
        hcp_id=hcp.id,
        interaction_type=data.interaction_type,
        date=data.date,
        time=data.time,
        attendees=data.attendees,
        topics_discussed=data.topics_discussed,
        outcomes=data.outcomes,
        follow_up_actions=data.follow_up_actions
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction

# AI Chat endpoint
from langchain_core.messages import HumanMessage

@app.post("/chat", response_model=schemas.AgentResponse)
def chat_with_agent(req: schemas.ChatRequest, db: Session = Depends(get_db)):
    # Initialize LangGraph state
    # In a real app we'd load previous messages and form state based on interaction_id
    # For this demo, we assume the frontend sends the whole context or we just process the new message
    
    state = {
        "messages": [HumanMessage(content=req.message)],
        "form_data": schemas.FormUpdateData()
    }
    
    # Run the graph
    try:
        app_result = agent.app_agent.invoke(state)
        # Extract final LLM chat response
        final_messages = app_result["messages"]
        bot_response = final_messages[-1].content
        # Extract updated form data (populated if tools were called)
        form_updates = app_result.get("form_data", None)
    except Exception as e:
        bot_response = f"Groq API Error: {str(e)}"
        form_updates = None

    
    return schemas.AgentResponse(
        chat_response=bot_response,
        form_updates=form_updates,
        interaction_id=req.interaction_id
    )
