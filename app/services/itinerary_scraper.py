import asyncio
import trafilatura
from typing import Optional, Dict
from playwright.async_api import async_playwright
import logging

logger = logging.getLogger(__name__)

class ItineraryScraper:
    """
    Service to scrape and curate travel itineraries from the web.
    Uses trafilatura for speed and Playwright for dynamic content.
    """

    @staticmethod
    async def scrape_url(url: str) -> Optional[Dict]:
        """
        Scrapes a single URL and returns curated content.
        """
        try:
            # 1. Try Trafilatura first (fastest, cleanest for blogs)
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                result = trafilatura.extract(
                    downloaded, 
                    include_links=True, 
                    include_images=True,
                    output_format='json'
                )
                if result:
                    import json
                    return json.loads(result)

            # 2. Fallback to Playwright if needed (for JS-heavy sites)
            return await ItineraryScraper._scrape_with_playwright(url)
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return None

    @staticmethod
    async def _scrape_with_playwright(url: str) -> Optional[Dict]:
        """
        Headless browser fallback for sites that block simple requests.
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Set a mobile-like user agent to avoid some blocks
            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"
            })

            try:
                await page.goto(url, wait_until="networkidle", timeout=30000)
                content = await page.content()
                
                # Use trafilatura on the rendered content
                result = trafilatura.extract(content, output_format='json')
                
                await browser.close()
                if result:
                    import json
                    return json.loads(result)
                    
            except Exception as e:
                logger.error(f"Playwright error for {url}: {str(e)}")
                await browser.close()
                
            return None

    @staticmethod
    def curate_itinerary_data(raw_data: Dict) -> Dict:
        """
        Takes raw scraped data and extracts key travel entities.
        (This will be expanded to use NLP or local heuristics)
        """
        if not raw_data:
            return {}

        return {
            "title": raw_data.get("title"),
            "source": raw_data.get("source"),
            "content": raw_data.get("text"),
            "metadata": {
                "author": raw_data.get("author"),
                "date": raw_data.get("date"),
                "hostname": raw_data.get("hostname")
            }
        }

# Example usage (commented out):
# if __name__ == "__main__":
#     url = "https://www.nomadicmatt.com/travel-guides/japan-travel-tips/tokyo/"
#     data = asyncio.run(ItineraryScraper.scrape_url(url))
#     print(ItineraryScraper.curate_itinerary_data(data))
