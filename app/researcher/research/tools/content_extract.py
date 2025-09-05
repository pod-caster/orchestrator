import asyncio
import logging
import pandas as pd
import trafilatura
from newspaper import Article
from urllib.parse import urlparse
from typing import List, Optional, Dict
from abc import ABC, abstractmethod
from ... import constant as constant
from crawl4ai import AsyncWebCrawler
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Logging configuration
logging.basicConfig(format="%(asctime)s: %(levelname)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# ------------------------
# Abstract Scraper Base
# ------------------------
class BaseScraper(ABC):
    """Abstract Scraper base class."""

    @abstractmethod
    async def extract(self, url: str) -> Optional[str]:
        """Extract content from a URL asynchronously."""
        pass


# ------------------------
# Concrete Scrapers
# ------------------------
class NewspaperScraper(BaseScraper):
    async def extract(self, url: str) -> Optional[str]:
        try:
            # run blocking newspaper3k in thread executor
            loop = asyncio.get_event_loop()

            def run_newspaper():
                article = Article(url)
                article.download()
                article.parse()
                return article.text.strip()

            return await loop.run_in_executor(None, run_newspaper)

        except Exception as e:
            logger.warning(f"[newspaper3k failed] {str(e)} | URL: {url}")
            return None


class TrafilaturaScraper(BaseScraper):
    async def extract(self, url: str) -> Optional[str]:
        try:
            loop = asyncio.get_event_loop()

            def run_trafilatura():
                downloaded = trafilatura.fetch_url(url)
                if downloaded:
                    return trafilatura.extract(downloaded).strip()
                return None

            return await loop.run_in_executor(None, run_trafilatura)

        except Exception as e:
            logger.warning(f"[trafilatura failed] {e} | URL: {url}")
            return None


class Crawl4AIScraper(BaseScraper):
    async def extract(self, url: str) -> Optional[str]:
        try:
            async with AsyncWebCrawler() as crawler:
                result = await crawler.arun(url=url)

            return result
        except Exception as e:
            logger.warning(f"[Crawl4AI failed] {str(e)} | URL: {url}")
            return None


# ------------------------
# Scraper Manager
# ------------------------
class ScraperManager:
    def __init__(self, priority: List[str] = constant.extraction_priority):
        self.priority = priority
        self.scraper_map: Dict[str, BaseScraper] = {
            "newspaper3k": NewspaperScraper(),
            "trafilatura": TrafilaturaScraper(),
            "crawl4ai": Crawl4AIScraper(),
        }
        self.logger = logger

    def is_wikipedia(self, url: str) -> bool:
        """Check if URL is a Wikipedia page."""
        return "wikipedia.org" in urlparse(url).netloc

    async def extract_single_url(self, url: str) -> Optional[str]:
        """Extract content from a single URL using scraper priority."""
        if self.is_wikipedia(url):
            self.logger.info(f"Skipping Wikipedia URL: {url}")
            return ""

        for scraper_name in self.priority:
            scraper = self.scraper_map.get(scraper_name)
            if scraper:
                content = await scraper.extract(url)
                if content and len(content) > 200:
                    self.logger.info(f"[Success with {scraper_name}] for {url}")
                    return content
        self.logger.warning(f"[All scrapers failed] {url}")
        return None

    async def extract_batch(self, urls: List[str]) -> Dict[str, Optional[str]]:
        """Asynchronously extract content from a batch of URLs."""
        tasks = [self.extract_single_url(url) for url in urls]
        results = await asyncio.gather(*tasks)
        return dict(zip(urls, results))

    async def extract_links(self, webresults: dict) -> List[Dict[str, Optional[str]]]:
        self.logger.info("Starting Extraction")
        links = webresults.get("web_results", [])
        wiki_content = webresults.get("wiki_content", [])
        output: List[Dict[str, Optional[str]]] = []

        if len(links) == 0 and len(wiki_content) == 0:
            raise ValueError("No links found in web_results")

        if len(links) > 0:
            link_df = pd.DataFrame(links)
            urls = link_df["link"].tolist()
            self.logger.info(f"Extracting content from {len(urls)} URLs...")

            content_map = await self.extract_batch(urls)
            output = [
                {"link": url, "content": content_map.get(url)}
                for url in urls
                if isinstance(content_map.get(url), str) and len(content_map.get(url)) > 0
            ]

        if len(wiki_content) > 0:
            output += wiki_content

        self.logger.info("Extraction complete.")
        return output
