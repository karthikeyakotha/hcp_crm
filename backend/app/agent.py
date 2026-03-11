import os
from typing import Annotated, TypedDict, List, Optional
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from .schemas import FormUpdateData
from dotenv import load_dotenv

load_dotenv()

# Configure Groq LLM
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(
    model="llama-3.1-8b-instant",  # Fastest and most efficient supported Groq model
    api_key=groq_api_key, 
    temperature=0
)

# ----------------- TOOLS -----------------

@tool
def log_interaction(
    hcp_name: str, 
    interaction_type: Optional[str] = None, 
    date: Optional[str] = None, 
    time: Optional[str] = None, 
    attendees: Optional[str] = None, 
    topics_discussed: Optional[str] = None, 
    outcomes: Optional[str] = None, 
    follow_up_actions: Optional[str] = None, 
    materials: Optional[List[str]] = None
) -> str:
    """
    Log a new interaction with an HCP. Call this when the user describes a new meeting or interaction.
    Extracts relevant fields from their message.
    """
    # This tool simulates creating/updating the active form on the frontend
    return f"Prepared log form for interaction with {hcp_name}."

@tool
def edit_interaction(
    topics_discussed: Optional[str] = None, 
    outcomes: Optional[str] = None, 
    follow_up_actions: Optional[str] = None, 
    materials: Optional[List[str]] = None
) -> str:
    """
    Edit the currently drafted interaction. Call this when the user adds more context to the current draft
    (e.g., 'Oh, also add that we gave them sample X' or 'Change the outcome to Y').
    """
    return "Edited interaction form."

@tool
def search_hcp_history(hcp_name: str) -> str:
    """
    Search past history or CRM logs for a specific HCP. 
    Use this to get context if the user asks 'When did I last meet Dr. Smith?'
    """
    # Mock return for assignment
    return f"Past history for {hcp_name}: Met on 2025-01-15, discussed Product A. Neutral sentiment."

@tool
def suggest_followups(topics: str) -> str:
    """
    Suggest follow-up activities based on the topics discussed.
    Call this when the user asks for suggestions or what to do next.
    """
    return f"Suggested follow-ups for topics ({topics}): 1. Email clinical study data. 2. Set up next meeting in 2 weeks."

@tool
def lookup_materials(query: str) -> str:
    """
    Search the internal product/campaign database for materials or samples to share.
    Use this when the user is unsure of a product's exact name.
    """
    return f"Found materials matching '{query}': Product X Brochure, Sample Pack Y."

# Bind tools
tools = [log_interaction, edit_interaction, search_hcp_history, suggest_followups, lookup_materials]
llm_with_tools = llm.bind_tools(tools)

# ----------------- STATE -----------------

class AgentState(TypedDict):
    messages: Annotated[list, "messages"]
    # We maintain the active form draft state in LangGraph
    form_data: FormUpdateData

# ----------------- GRAPH -----------------

def call_model(state: AgentState):
    messages = state["messages"]

    sys_msg = SystemMessage(content="""
You are an AI assistant in a Life Sciences CRM helping field reps log interactions with Healthcare Professionals (HCPs).
You MUST use your tools to parse the user's input and update the CRM form.
If they say 'I met Dr. Smith today, discussed Product X', you should call `log_interaction`.
If they later say 'Add that I gave him a sample', call `edit_interaction`.

You can also use tools to look up past history, suggest follow-ups, or search materials if asked.
Provide a brief, confirming conversational response after calling a tool.
""")
    
    response = llm_with_tools.invoke([sys_msg] + messages)
    return {"messages": [response]}

# Tool execution node (custom wrapper to also extract form data for UI updates)
def call_tools(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    
    tool_responses = []
    form_update = state.get("form_data", FormUpdateData())

    for tool_call in last_message.tool_calls:
        # Determine which tool was called
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        # If it's modifying the form, update our state
        if tool_name == "log_interaction" or tool_name == "edit_interaction":
            update_dict = form_update.model_dump(exclude_unset=True)
            for k, v in tool_args.items():
                if v is not None:
                    update_dict[k] = v
            # Re-instantiate
            form_update = FormUpdateData(**update_dict)

        # Basic router logic to call the actual function
        result_str = "Tool not found"
        if tool_name == "log_interaction":
            result_str = log_interaction.invoke(tool_args)
        elif tool_name == "edit_interaction":
            result_str = edit_interaction.invoke(tool_args)
        elif tool_name == "search_hcp_history":
            result_str = search_hcp_history.invoke(tool_args)
        elif tool_name == "suggest_followups":
            result_str = suggest_followups.invoke(tool_args)
        elif tool_name == "lookup_materials":
            result_str = lookup_materials.invoke(tool_args)

        tool_msg = ToolMessage(content=result_str, tool_call_id=tool_call["id"], name=tool_name)
        tool_responses.append(tool_msg)
        
    return {"messages": tool_responses, "form_data": form_update}

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# Build Graph
graph = StateGraph(AgentState)
graph.add_node("agent", call_model)
graph.add_node("tools", call_tools)

graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")

app_agent = graph.compile()
