import httpx
import logging
import json
import redis.asyncio as redis
from typing import List, Dict
from app.core.config import settings

logger = logging.getLogger(__name__)

class KnowledgeHarvester:
    """
    Ingests and synthesizes expertise, utilizing Redis caching
    to guarantee blazing fast sub-second response times.
    """

    def __init__(self):
        self.serper_key = settings.SERPER_API_KEY
        self.forum_domains = "site:reddit.com OR site:tripadvisor.com/ShowForum"
        # Connect to our local Redis container
        self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

    async def find_expert_nuggets(self, query: str, depth: str = "deep") -> List[str]:
        """
        Dynamic Harvester:
        depth='light' -> 1 API call, fast surface level facts (e.g., 'What time does the museum open?')
        depth='deep'  -> 3 parallel API calls, deep forum research (e.g., 'Hidden gems in Tokyo')
        """
        cache_key = f"harvester:{depth}:{query.replace(' ', '_').lower()}"
        
        # 1. TRY CACHE (5 milliseconds)
        try:
            cached_result = await self.redis_client.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
        except Exception as e:
            logger.warning(f"Redis cache error: {e}")

        if not self.serper_key:
            return ["Live search is currently offline."]

        async with httpx.AsyncClient() as client:
            try:
                tasks = []
                
                # Base Fact Search (Always runs)
                tasks.append(
                    client.post(
                        "https://google.serper.dev/search",
                        headers={"X-API-KEY": self.serper_key, "Content-Type": "application/json"},
                        json={"q": f"{query} authentic non touristy tips", "num": 2}
                    )
                )

                # Heavy Deep Dive (Only runs if intent requires it)
                if depth == "deep":
                    tasks.append(
                        client.post(
                            "https://google.serper.dev/search",
                            headers={"X-API-KEY": self.serper_key, "Content-Type": "application/json"},
                            json={"q": f"{query} {self.forum_domains}", "num": 3}
                        )
                    )
                    tasks.append(
                        client.post(
                            "https://google.serper.dev/search",
                            headers={"X-API-KEY": self.serper_key, "Content-Type": "application/json"},
                            json={"q": f"{query} what to avoid tourist traps safety", "num": 2}
                        )
                    )
                
                import asyncio
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                nuggets = []
                labels = ["[FORUM TRUTH]", "[HIDDEN GEM]", "[VIBE CHECK]"]
                
                # Synthesize the 100-hours of research into a dense context block
                for i, res in enumerate(results):
                    if not isinstance(res, Exception) and res.status_code == 200:
                        for item in res.json().get("organic", []):
                            snippet = item.get("snippet", "")
                            nuggets.append(f"{labels[i]} - {snippet}")
                
                # 3. SAVE TO CACHE (TTL: 7 Days = 604800 seconds)
                try:
                    await self.redis_client.set(cache_key, json.dumps(nuggets), ex=604800)
                except Exception as e:
                    logger.warning(f"Redis save error: {e}")
                    
                return nuggets
            except Exception as e:
                logger.error(f"Deep Dive Error: {str(e)}")
                return []


harvester = KnowledgeHarvester()
