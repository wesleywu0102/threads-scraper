import asyncio
import json
from threads_scraper import ThreadsScraper, ScraperConfig

async def main():
    scraper = ThreadsScraper()
    results = await scraper.scrape_search("python programming", days=7)
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
