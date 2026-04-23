import asyncio
import logging
from typing import List
from app.services.itinerary_scraper import ItineraryScraper
from app.services.rag_service import rag_service
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def curate_travel_knowledge(urls: List[str]):
    """
    Bulk scrape and ingest travel URLs into the RAG system.
    """
    scraper = ItineraryScraper()
    
    for url in urls:
        logger.info(f"🚀 Processing: {url}")
        
        # 1. Scrape
        data = await scraper.scrape_url(url)
        if not data:
            logger.warning(f"⚠️ Failed to scrape: {url}")
            continue
            
        curated = scraper.curate_itinerary_data(data)
        text_content = curated.get("content")
        
        if not text_content:
            logger.warning(f"⚠️ No text content found for: {url}")
            continue

        # 2. Structure & Ingest into RAG
        # We add the metadata for better source citation in the AI chat
        metadata = curated.get("metadata", {})
        metadata["url"] = url
        metadata["title"] = curated.get("title")
        
        try:
            # The rag_service handles chunking and embedding internally
            rag_service.add_documents(
                texts=[text_content],
                metadatas=[metadata]
            )
            logger.info(f"✅ Successfully ingested: {curated.get('title')}")
        except Exception as e:
            logger.error(f"❌ Error ingesting {url}: {str(e)}")

async def main():
    # Example curated URL list - you can expand this to 100s of URLs
    curated_sources = [
        "https://www.nomadicmatt.com/travel-guides/japan-travel-tips/tokyo/",
        "https://www.thecrazytourist.com/15-best-things-to-do-in-tokyo-japan/",
        "https://www.timeout.com/tokyo/things-to-do/best-things-to-do-in-tokyo",
        "https://www.lonelyplanet.com/japan/tokyo/attractions"
    ]
    
    await curate_travel_knowledge(curated_sources)

if __name__ == "__main__":
    asyncio.run(main())
