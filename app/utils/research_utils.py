import logging
import app.constant as constant
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()    
logger.setLevel(logging.INFO)




def prepare_input_for_research(input_dict):
    mode = input_dict.get("scraper_mode")
    supported_modes = constant.config.get("modes")
    if mode not in supported_modes:
        logger.warning(f"Unsupported mode '{mode}' provided. Defaulting to 'research' mode.")
        mode = "researcher"

    if mode == "researcher":
        research_configs = constant.research_config
        return {
            "topic": input_dict.get("topic"),
            "research_configs": research_configs
        }

    elif mode == "user":
        raise ValueError("User mode is not supported for the time being.")     
