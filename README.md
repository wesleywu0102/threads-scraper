# Threads Scraper

A Python web scraper for Threads.net using Playwright.

## Features

- Asynchronous web scraping with Playwright
- Type hints for better code maintainability
- Comprehensive error handling and logging
- Easy configuration and extensibility
- Search functionality for Threads.net content

## Installation

### Prerequisites
- Python 3.9 or higher
- Poetry for dependency management

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/wesleywu0102/threads-scraper.git
   ```
2. Navigate to the project directory:
   ```bash
   cd threads-scraper
   ```
3. Install dependencies:
   ```bash
   poetry install
   ```
4. Install Playwright browsers:
   ```bash
   poetry run playwright install chromium
   ``` 

## Usage

Basic example:

```python
import asyncio
from threads_scraper import ThreadsScraper

async def main():
    url = "https://www.threads.net/search?q=example"
    scraper = ThreadsScraper()
    results = await scraper.scrape_data(url)
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
```

## Development

1. Set up the development environment:
```bash
poetry install
```

2. Run tests:
```bash
poetry run pytest
```

3. Check code style:
```bash
poetry run ruff check .
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Playwright](https://playwright.dev/)
- Inspired by the need for efficient Threads.net data collection 
