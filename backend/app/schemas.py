import datetime
from typing import List, Optional
from pydantic import BaseModel

# Material Schemas
class MaterialBase(BaseModel):
    name: str
    type: str

class MaterialCreate(MaterialBase):
    pass

class MaterialOut(MaterialBase):
    id: int
    class Config:
        from_attributes = True

# HCP Schemas
class HCPBase(BaseModel):
    name: str
    specialty: Optional[str] = None
    contact_info: Optional[str] = None

class HCPCreate(HCPBase):
    pass

class HCPOut(HCPBase):
    id: int
    class Config:
        from_attributes = True

# Interaction Schemas
class InteractionBase(BaseModel):
    interaction_type: Optional[str] = None
    date: Optional[datetime.date] = None
    time: Optional[datetime.time] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    outcomes: Optional[str] = None
    follow_up_actions: Optional[str] = None

class InteractionCreate(InteractionBase):
    hcp_name: str # Client can just pass HCP name and it will lookup/create
    materials: List[str] = []

class InteractionUpdate(InteractionBase):
    hcp_name: Optional[str] = None
    materials: Optional[List[str]] = None

class InteractionOut(InteractionBase):
    id: int
    hcp: HCPOut
    materials_shared: List[MaterialOut] = []

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    interaction_id: Optional[int] = None # the context of which form we are actively filling out

# AI response format used by UI
class FormUpdateData(BaseModel):
    hcp_name: Optional[str] = None
    interaction_type: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    outcomes: Optional[str] = None
    follow_up_actions: Optional[str] = None
    materials: Optional[List[str]] = None

class AgentResponse(BaseModel):
    chat_response: str
    # When the agent decides to update the form, it will populate this
    form_updates: Optional[FormUpdateData] = None
    interaction_id: Optional[int] = None
