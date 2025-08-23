import pandas as pd
from .research.tools.content_extract import URLExtractor
from .research.research_agent import ResearchAgent

import logging

# Logging configuration
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def prepare_output(status, content):
    return {"status": status, "output": content}

async def extract(topic, research_configs):
    try:
        logger.info(f"Starting Content Extraction for topic {topic}")
        researcher = ResearchAgent()
        url_extractor = URLExtractor()
        logger.info(f"Researching about {topic}")
        url_content = await researcher.research(topic, research_configs)
        logger.info(f"Done Researching about {topic}")

        logger.info(f"Extracting content from links researched about {topic}")
        extracted_content = await url_extractor.extract_links(url_content)
        logger.info(f"Done extracting content")

        status = "Success"
        output = prepare_output(status, extracted_content)

    except Exception as e:
        logger.error(f"Error occured while extracting {str(e)}")
        status = "Failure"
        extracted_content = []
        output = prepare_output(status, extracted_content)

    finally:
        return output
    