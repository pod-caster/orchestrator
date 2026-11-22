from app.researcher.extract import research_and_extract, scrape
import time
import logging
# Logging configuration
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
class ResearchService:
    async def run(self, topic, research_configs):
        logger.info(f"Running Research Service for topic {topic}")
        start = time.time()
        output = await research_and_extract(topic, research_configs)
        end = time.time()
        logger.info(f"Research Service completed in {round(end - start, 2)} seconds")   
        return output

class ScraperService:
    async def run(self, links:list[str]):
        logger.info(f"Running Scraper Service for links {links}")
        start = time.time()
        output = await scrape(url_list = links)
        end = time.time()
        logger.info(f"Scraper Service completed in {round(end - start, 2)} seconds")   
        return output