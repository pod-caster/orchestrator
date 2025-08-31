import asyncio
from newspaper import Article
import trafilatura
from urllib.parse import urlparse
from typing import List, Optional, Dict
from ... import constant as constant
import pandas as pd
import logging

# Logging configuration
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class URLExtractor:
    def __init__(self, priority: List[str] = constant.extraction_priority):
        self.priority = priority
        self.scraper_map = {
            "newspaper3k": self.extract_with_newspaper,
            "trafilatura": self.extract_with_trafilatura,
        }
        self.logger = logger

    def is_wikipedia(self, url: str) -> bool:
        """Check if URL is a Wikipedia page."""
        return "wikipedia.org" in urlparse(url).netloc

    def extract_with_newspaper(self, url: str) -> Optional[str]:
        """Extract content using newspaper3k."""
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.text.strip()
        except Exception as e:
            self.logger.warning(f"[newspaper3k failed] {e} | URL: {url}")
            return None

    def extract_with_trafilatura(self, url: str) -> Optional[str]:
        """Extract content using trafilatura."""
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                return trafilatura.extract(downloaded).strip()
            return None
        except Exception as e:
            self.logger.warning(f"[trafilatura failed] {e} | URL: {url}")
            return None

    def extract_single_url(self, url: str) -> Optional[str]:
        """Extract content from a single URL using scraper priority."""
        if self.is_wikipedia(url):
            self.logger.info(f"Skipping Wikipedia URL: {url}")
            return ""

        for scraper_name in self.priority:
            scraper_fn = self.scraper_map.get(scraper_name)
            if scraper_fn:
                content = scraper_fn(url)
                if content and len(content) > 200:
                    self.logger.info(f"[Success with {scraper_name}] for {url}")
                    return content
        self.logger.warning(f"[All scrapers failed] {url}")
        return None

    async def extract_batch(self, urls: List[str]) -> Dict[str, Optional[str]]:
        """Asynchronously extract content from a batch of URLs."""
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(None, self.extract_single_url, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return dict(zip(urls, results))

    async def extract_links(self, webresults: dict) -> List[Dict[str, Optional[str]]]:
        self.logger.info("Starting Extraction")
        links = webresults.get("web_results", [])
        wiki_content = webresults.get("wiki_content", [])
        output = [
        ]
        if len(links) == 0 and len(wiki_content) == 0:
            raise ValueError("No links found in web_results")

        if len(links) > 0:
            link_df = pd.DataFrame(links)
            urls = link_df['link'].tolist()

            self.logger.info(f"Extracting content from {len(urls)} URLs...")

            content_map = await self.extract_batch(urls)

            output = [{"link": url, "content": content_map.get(url)} for url in urls if isinstance(content_map.get(url), str) and len(content_map.get(url)) > 0]

        if len(wiki_content) > 0:
            output += wiki_content

        self.logger.info("Extraction complete.")

        return output
