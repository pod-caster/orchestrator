from app.researcher.extract import extract
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
        output = await extract(topic, research_configs)
        end = time.time()
        logger.info(f"Research Service completed in {round(end - start, 2)} seconds")   
        return output
