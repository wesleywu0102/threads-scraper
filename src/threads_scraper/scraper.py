import json
import logging
import asyncio
from typing import List, Dict, Any
from pathlib import Path
from dataclasses import dataclass
from parsel import Selector
from playwright.async_api import async_playwright, Page, Browser, BrowserContext, Error as PlaywrightError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ScraperConfig:
    """Scraper configuration class"""
    viewport_width: int = 1920
    viewport_height: int = 1080
    selector_wait: str = "[data-pressable-container=true]"

class ThreadsScraper:
    """Threads website scraper class"""
    
    def __init__(self, config: ScraperConfig = ScraperConfig()):
        self.config = config

    async def _setup_browser(self) -> tuple[Browser, BrowserContext, Page]:
        """Set up browser environment"""
        try:
            playwright = await async_playwright().start()
            browser = await playwright.chromium.launch()
            context = await browser.new_context(
                viewport={
                    "width": self.config.viewport_width, 
                    "height": self.config.viewport_height
                }
            )
            page = await context.new_page()
            return browser, context, page
        except PlaywrightError as e:
            logger.error(f"Browser setup failed: {str(e)}")
            raise

    def _extract_datasets(self, page_content: str) -> List[Dict[str, Any]]:
        """Extract data from page content"""
        selector = Selector(page_content)
        hidden_datasets = selector.css('script[type="application/json"][data-sjs]::text').getall()
        
        relevant_datasets = []
        for hidden_dataset in hidden_datasets:
            if '"ScheduledServerJS"' not in hidden_dataset or "thread_items" not in hidden_dataset:
                continue
            try:
                data = json.loads(hidden_dataset)
                relevant_datasets.append(data)
            except json.JSONDecodeError as e:
                logger.warning(f"JSON parsing error: {str(e)}")
                continue
        
        return relevant_datasets

    async def scrape_data(self, url: str) -> List[Dict[str, Any]]:
        """
        Main method for scraping Threads website data
        
        Args:
            url: Target webpage URL
            
        Returns:
            List containing scraped data
            
        Raises:
            PlaywrightError: Browser operation related errors
        """
        browser = None
        try:
            async with async_playwright() as pw:
                browser = await pw.chromium.launch()
                context = await browser.new_context(
                    viewport={
                        "width": self.config.viewport_width, 
                        "height": self.config.viewport_height
                    }
                )
                page = await context.new_page()
                
                await page.goto(url)
                await page.wait_for_selector(self.config.selector_wait)
                
                datasets = self._extract_datasets(await page.content())
                logger.info(f"Successfully scraped {len(datasets)} items from {url}")
                
                # Properly close all resources
                await page.close()
                await context.close()
                await browser.close()
                
                return datasets
                    
        except PlaywrightError as e:
            logger.error(f"Scraping process error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise
        finally:
            if browser:
                try:
                    await browser.close()
                except Exception:
                    pass

async def main():
    """Main function"""
    import sys
    import io
    
    # Set stdout encoding to UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    url = "https://www.threads.net/search?days=30&q=%E8%90%AC%E5%AF%A7&serp_type=default"
    scraper = ThreadsScraper()
    
    try:
        result = await scraper.scrape_data(url)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        logger.error(f"Program execution failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"Program execution error: {str(e)}")
        sys.exit(1)