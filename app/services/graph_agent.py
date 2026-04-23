import operator
from typing import Annotated, List, Dict, Sequence, TypedDict, Union
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from app.services.arbiter import arbiter
from app.services.corporate_policy import policy_engine
from app.services.itinerary_scraper import ItineraryScraper
from app.core.config import settings

from app.core.logic_engine import expert_engine, UserTravelProfile, VisaRequirement

# Define the state of our agent
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    user_profile: UserPreferenceMap
    visa_info: Optional[VisaRequirement]
    
    # Discovery Progress
    discovery_completed: bool = False
    budget_feasibility_score: float = 0.0 # 0.0 to 1.0
    
    context_tags: List[str]
    is_business: bool
    data_results: List[Dict]
    activities: List[TrotterActivity]
    itinerary_route: List[str] # List of neighborhood sequences
    policy_violations: List[str]

from app.services.harvester import harvester
from app.services.logistics_engine import logistics_engine
from app.services.memory_summarizer import memory_compressor

# 1. Define Dynamic Tools for the LLM
@tool
async def search_expert_secrets_tool(location: str, interest: str):
    """Deep-dives into travel blogs to find 'Hidden Gems' and 'Expert Secrets' for a location."""
    query = f"best {interest} secrets in {location}"
    return await harvester.find_expert_nuggets(query)

@tool
async def search_flights_tool(origin_iata: str, destination_iata: str, date: str):
    """Search for real-time flight offers. Use IATA codes (e.g. JFK)."""
    return await arbiter.find_best_flight(origin_iata, destination_iata, date)

@tool
async def search_hotels_tool(city: str, check_in_date: str, check_out_date: str):
    """Search for hotels in a specific city for given dates."""
    return await arbiter.find_best_hotel(city, check_in_date, check_out_date)

class TrotterGraphBrain:
    def __init__(self):
        # The Master Agent (Expensive, Slow, Brilliant) - strict JSON mode to protect UI
        self.master_llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name="llama-3.3-70b-versatile",
            model_kwargs={"response_format": {"type": "json_object"}}
        ).bind_tools([search_flights_tool, search_hotels_tool, search_expert_secrets_tool])
        
        # The Triage Agent (Cheap, Fast, Simple)
        self.fast_llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name="llama3-8b-8192"
        )
        
        self.workflow = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(AgentState)

        # Nodes
        workflow.add_node("agent", self._call_model)
        workflow.add_node("tools", ToolNode([search_flights_tool, search_hotels_tool, search_expert_secrets_tool]))
        workflow.add_node("policy_guard", self._policy_node)
        workflow.add_node("optimizer", self._itinerary_optimizer_node) # OUR NEW EXPERT NODE
        
        # Edges
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges("agent", self._should_continue)
        workflow.add_edge("tools", "policy_guard")
        workflow.add_edge("policy_guard", "optimizer") # Route through optimizer
        workflow.add_edge("optimizer", "agent")

        return workflow.compile()

    async def _call_model(self, state: AgentState):
        """Dynamic LLM call with Cascading Router and Semantic Compression."""
        
        # 1. ZERO-COST COMPRESSION: Stop token bloat if chat gets too long
        compressed_messages = await memory_compressor.compress_history(list(state["messages"]))
        
        profile = state.get("user_profile", UserPreferenceMap())
        visa = state.get("visa_info")
        
        # Inject our 'Moat' Context
        expert_context = f"""
        EXPERT CONTEXT:
        - Travel Archetype: {profile.archetype if hasattr(profile, 'archetype') else 'Unknown'}
        - Must Haves: {profile.must_haves}
        - Dealbreakers: {profile.hard_dealbreakers}
        Please output your final itinerary payload in strict JSON format.
        """
        
        messages = [SystemMessage(content=expert_context)] + compressed_messages
        
        # 2. MODEL CASCADING ROUTER: Intelligently select compute size
        user_intent = messages[-1].content.lower()
        
        # If it's a simple chat/greeting, use the penny-cost model
        if len(user_intent.split()) < 10 and "plan" not in user_intent and "book" not in user_intent:
            response = await self.fast_llm.ainvoke(messages)
        else:
            # Complex travel request -> Unlock Master Agent
            response = await self.master_llm.ainvoke(messages)
            
        return {"messages": [response]}

    def _should_continue(self, state: AgentState):
        """Logic to determine if the agent moves to Research or stays in Discovery."""
        # Expert Guardrail: If we don't know the basics, we don't search.
        messages = state["messages"]
        last_message = messages[-1]
        
        # If the LLM has already decided to use a tool, it's passed discovery
        if last_message.tool_calls:
            return "tools"
            
        # Check if we have the Big 4 (Who, Where, What, Budget)
        # (Simplified heuristic for the demo graph)
        if len(messages) < 3:
            return END # Stay in conversation to get intake info
            
        return END

    async def _itinerary_optimizer_node(self, state: AgentState):
        """
        Expert Logic: Performs geographic routing and age-sensitivity checks.
        Ensures a 'Single Flow' route and appropriate intensity.
        NOW INCLUDES ANTICIPATORY LOGISTICS
        """
        print("--- OPTIMIZING ROUTE & PERSONA FIT ---")
        user_age = state.get("user_profile", {}).get("age", 25)
        
        # 1. Geographic Re-ordering (Logical Flow)
        optimized_activities = sorted(state.get("activities", []), key=lambda x: getattr(x, 'neighborhood', 'Unknown'))

        # 2. Add Arrival Protocol and Friction Buffers via Logistics Engine
        mock_itinerary_day = {"is_arrival_day": True, "activities": [act.__dict__ for act in optimized_activities if hasattr(act, '__dict__')]}
        logistics_engine.apply_arrival_rest_protocol(mock_itinerary_day)
        
        # Find 'Companion Hours'
        flexible_blocks = logistics_engine.identify_empty_hours(state.get("data_results", []))

        # Pass findings back via System warning to LLM
        if flexible_blocks:
            alert = f"Logistics System Note: Identified {len(flexible_blocks)} empty blocks. Tell user Trotter will manage these on the fly."
            state["messages"].append(SystemMessage(content=alert))

        return {"activities": optimized_activities}

    async def run(self, query: str, is_business: bool = False):
        """Entry point to run the dynamic graph brain."""
        initial_state = {
            "messages": [
                SystemMessage(content="You are Trotter AI, a professional travel concierge. Use tools to find real-time data before answering."),
                HumanMessage(content=query)
            ],
            "is_business": is_business,
            "data_results": [],
            "policy_violations": []
        }
        return await self.workflow.ainvoke(initial_state)

graph_brain = TrotterGraphBrain()
