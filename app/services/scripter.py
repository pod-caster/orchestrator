from app.scripter.handler import main_function
import time
import logging
# Logging configuration
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ScripterService:
    async def run(self, topic, extracted_content, script_configs):
        logger.info(f"Running Scripter Service for topic {topic}")
        start = time.time()
        output = await main_function(topic, script_configs, extracted_content)
        end = time.time()
        logger.info(f"Scripter Service completed in {round(end - start, 2)} seconds")   
        return output