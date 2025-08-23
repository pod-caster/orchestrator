import pandas as pd

import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from .scripting.script_agent import SciptAgent

async def main_function(topic,script_configs, content):
    content_df = pd.DataFrame(content)
    
    # Initialize the script agent with the topic, script configurations, and content DataFrame
    logger.info(f"Initializing script agent for topic: {topic}")
    agent = SciptAgent(topic, script_configs, content_df)
    script = await agent.run_scripter()
    logger.info(f"Script generation completed for topic: {topic}")

    # 
    return script