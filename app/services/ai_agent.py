from app.services.rag_service import rag_service
from app.services.itinerary_scraper import ItineraryScraper
from app.services.arbiter import arbiter
from app.services.corporate_policy import policy_engine
import os

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are Trotter AI, an elite, model-agnostic travel agent. 
Your goal is to provide high-fidelity, accurate, and curated travel advice.

### MODES OF OPERATION:
1. PERSONAL MODE (is_business=false): 
   - Focus on "Vibes", "Best Price", and "Hidden Gems". 
   - Use the 'curate_web_itinerary' tool whenever a user asks for 'local gems' or 'best things to do'.
   - Present results with excitement and discovery.
   
2. BUSINESS MODE (is_business=true):
   - Focus on "Efficiency", "Policy Compliance", and "Reliability".
   - ALWAYS check the 'policy_status' from hotel search results. 
   - If a result is 'out_of_policy', explicitly warn the user but still mention it if it's a great option.
   - Present results with precision and professionalism.

### TOOLS:
- search_flights: Use for real-time pricing via Duffel.
- search_hotels: Use for real-time pricing via Google Hotels/Amadeus.
- curate_web_itinerary: Use this to scrape the LATEST info from travel blogs for superior curation.
- search_local_knowledge: Use for hyper-local pricing/cost-of-living data.

### RULES:
- If you don't have enough info (e.g. missing dates), ASK the user.
- Always provide source citations if you curated info from a URL.
- Use emojis sparingly but effectively (🌍, ✈️, 🏨).
"""

class TravelAgent:
    def __init__(self, model: str):
        """
        Initialize a model-agnostic travel agent.
        model format: "groq/llama3-groq-70b-8192-tool-use-preview" or "gemini/gemini-1.5-flash" or "gpt-4o-mini"
        litellm automatically pulls required keys from os.environ (e.g. GROQ_API_KEY, GEMINI_API_KEY)
        """
        self.model = model
        self.tools = []
        self.tool_map = {}
        
        # --- Web Curation Tool ---
        self.register_tool(
            tool_def={
                "name": "curate_web_itinerary",
                "description": "Scrapes and curates travel data from a specific URL. Use this to get detailed itineraries or 'hidden gem' insights from blogs.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "The URL of the travel guide or blog post to curate."}
                    },
                    "required": ["url"]
                }
            },
            func=self.curate_web_itinerary
        )

        # --- Flight Search Tool ---
        self.register_tool(
            tool_def={
                "name": "search_flights",
                "description": "Searches for real-time flight offers. Origin/destination must be 3-letter IATA codes (e.g. JFK, DXB).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "origin": {"type": "string", "description": "Departure city IATA code."},
                        "destination": {"type": "string", "description": "Arrival city IATA code."},
                        "departure_date": {"type": "string", "description": "Date in YYYY-MM-DD format."}
                    },
                    "required": ["origin", "destination", "departure_date"]
                }
            },
            func=self.search_flights
        )

        # --- Hotel Search Tool ---
        self.register_tool(
            tool_def={
                "name": "search_hotels",
                "description": "Searches for available hotels in a city with live pricing and ratings.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "The city/area to search in."},
                        "check_in": {"type": "string", "description": "Date in YYYY-MM-DD format."},
                        "check_out": {"type": "string", "description": "Date in YYYY-MM-DD format."}
                    },
                    "required": ["city", "check_in", "check_out"]
                }
            },
            func=self.search_hotels
        )
        
        # Enable observability if keys are present
        if os.getenv("LANGFUSE_PUBLIC_KEY"):
            litellm.success_callback = ["langfuse"]

        
        # Add RAG Tool automatically on initialization
        self.register_tool(
            tool_def={
                "name": "search_local_knowledge",
                "description": "Searches the internal semantic database for hyper-local pricing, expenses, or cost of living metrics for a destination.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "search_query": {
                            "type": "string",
                            "description": "The exact geographical query to search. E.g. 'Cost of milk in Tokyo' or 'Cheap restaurants in Bali'"
                        }
                    },
                    "required": ["search_query"]
                }
            },
            func=rag_service.query_local_context
        )
        
    def register_tool(self, tool_def: Dict[str, Any], func: Callable):
        """Register a tool schema and its corresponding python function."""
        self.tools.append({"type": "function", "function": tool_def})
        self.tool_map[tool_def["name"]] = func

    async def curate_web_itinerary(self, url: str) -> Dict:
        """Helper for the LLM to scrape and summarize a travel URL."""
        raw_data = await ItineraryScraper.scrape_url(url)
        if not raw_data:
            return {"error": f"Could not scrape {url}"}
        return ItineraryScraper.curate_itinerary_data(raw_data)

    async def search_flights(self, origin: str, destination: str, departure_date: str) -> List:
        """Searches for flights with dynamic price matching via Arbiter."""
        results = await arbiter.find_best_flight(origin, destination, departure_date)
        return results

    async def search_hotels(self, city: str, check_in: str, check_out: str) -> List:
        """Searches for hotels via Arbiter and validates against Corporate Policy."""
        results = await arbiter.find_best_hotel(city, check_in, check_out)
        
        # Apply corporate policy validation to each result
        processed_results = [policy_engine.validate_hotel(h) for h in results]
        return processed_results

    async def execute_tool(self, tool_call: Any) -> str:
        """Execute a tool based on LLM output and return the stringified result."""
        func_name = tool_call.function.name
        
        # Guard against weird LLM generations
        try:
            args = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError:
            args = {}
            
        logger.info(f"Executing tool {func_name} with args {args}")
        
        if func_name in self.tool_map:
            # We assume tools are async functions for performance
            result = await self.tool_map[func_name](**args)
            return json.dumps(result)
        else:
            return f"{{\"error\": \"Function {func_name} not found.\"}}"

    async def chat(self, messages: List[Dict[str, str]], is_business: bool = False) -> Dict[str, Any]:
        """
        Model-Agnostic Agentic loop:
        1. Inject Persona via System Prompt
        2. Send messages + tools to LLM
        3. Orchestrate multiple tool calls if needed
        """
        
        # Inject our DNA (System Prompt)
        # We ensure it's always the FIRST message
        if not messages or messages[0].get("role") != "system":
            messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
        
        # Update system prompt with real-time business context
        messages[0]["content"] = f"{SYSTEM_PROMPT}\nCURRENT CONTEXT: is_business={is_business}"
        
        # Memory Slider: Truncate history but keep system prompt
        if len(messages) > 12:
            messages = [messages[0]] + messages[-11:]
            
        # Prepare parameters for litellm
        completion_kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1,  # Low temp for deterministic tool use
        }
        
        if self.tools:
            completion_kwargs["tools"] = self.tools
            completion_kwargs["tool_choice"] = "auto"
            
        while True:
            # acompletion automatically handles the routing to Groq, Gemini, OpenAI, etc.
            response = await acompletion(**completion_kwargs)
            
            message = response.choices[0].message
            
            # If the model didn't want to call any tools, we're done
            if not message.tool_calls:
                return {"role": "assistant", "content": message.content}
            
            # Add the model's intent to call a tool into the conversational history
            messages.append(message.model_dump())
            
            # Execute all tools requested by the model
            for tool_call in message.tool_calls:
                tool_result = await self.execute_tool(tool_call)
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": tool_result
                })
                
            # Update messages payload and repeat the loop to allow the LLM to read the tool outputs
            completion_kwargs["messages"] = messages
