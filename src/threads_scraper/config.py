from dataclasses import dataclass
from typing import Optional

@dataclass
class ScraperConfig:
    """Scraper configuration class"""
    viewport_width: int = 1920
    viewport_height: int = 1080
    selector_wait: str = "[data-pressable-container=true]"
    headless: bool = True  # Run browser in headless mode
    timeout: int = 30000   # Page load timeout in milliseconds
    user_agent: Optional[str] = None  # Custom user agent
