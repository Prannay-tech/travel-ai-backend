from typing import List
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_groq import ChatGroq
from app.core.config import settings

class TrotterMemoryCompressor:
    """
    Prevents token-bloat and 'Amnesia' by compressing long chat histories
    into dense, zero-fluff semantic summaries.
    """
    
    def __init__(self):
        # We use the fastest, cheapest model for compression tasks 
        # (Llama-3-8B is pennies per million tokens)
        self.fast_llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name="llama3-8b-8192"
        )
        
    async def compress_history(self, messages: List[BaseMessage], max_turns: int = 6) -> List[BaseMessage]:
        """
        If chat history exceeds max_turns, it extracts core facts and replaces
        the old history with a dense summary, capping the LLM payload cost permanently.
        """
        if len(messages) <= max_turns:
            return messages
            
        # Extract the old messages to summarize
        old_messages = messages[:-4] # Keep the 4 most recent turns intact
        recent_messages = messages[-4:]
        
        prompt = "Summarize the key travel preferences, selected cities, budget, and dislikes from this conversation. Keep it extremely brief and factual."
        
        # Append the old messages for context
        summarization_payload = [SystemMessage(content=prompt)] + old_messages
        
        summary_response = await self.fast_llm.ainvoke(summarization_payload)
        
        # Create the new compressed state
        compressed_state = [
            SystemMessage(content=f"PREVIOUS CONVERSATION CONTEXT: {summary_response.content}")
        ] + recent_messages
        
        return compressed_state

memory_compressor = TrotterMemoryCompressor()
