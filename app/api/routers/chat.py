from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Dict, Any
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.services.graph_agent import graph_brain
from app.core.config import settings
from app.models.api import ChatMessage

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
# Register Duffel Tool
agent.register_tool(
    tool_def={
        "name": "search_flights",
        "description": "Search for real-time flight offers using origin, destination, and date.",
        "parameters": {
            "type": "object",
            "properties": {
                "origin": {
                    "type": "string",
                    "description": "IATA Airport code of origin (e.g. LHR, JFK)"
                },
                "destination": {
                    "type": "string",
                    "description": "IATA Airport code of destination (e.g. CDG)"
                },
                "date": {
                    "type": "string",
                    "description": "Departure date in YYYY-MM-DD format"
                },
                "passengers": {
                    "type": "integer",
                    "description": "Number of adult passengers"
                }
            },
            "required": ["origin", "destination", "date"]
        }
    },
    func=duffel_service.search_flights
)


@router.post("/")
@limiter.limit("20/minute")
async def chat_endpoint(request: Request, payload: ChatMessage):
    """
    Advanced LangGraph-powered chat endpoint.
    Handles Personal/Business logic through a cyclical state graph.
    """
    try:
        # Run the LangGraph State Machine
        result = await graph_brain.run(
            query=payload.message, 
            is_business=payload.is_business
        )
        
        # The last message in the graph state's 'messages' list is the AI response
        final_response = result["messages"][-1].content
        
        return {
            "response": final_response,
            "metadata": {
                "violations": result.get("policy_violations", []),
                "results": result.get("data_results", [])
            }
        }
    except Exception as e:
        logger.error(f"Graph execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail="The Trotter brain hit a snag. Please try again.")
