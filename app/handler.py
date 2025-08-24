from .services.researcher import ResearchService
from .services.scripter import ScripterService
from .services.tts import TTSService
from .model.request_model import PodcasterInput
from .utils.helper import convert_input_to_dict
from .utils.research_utils import prepare_input_for_research, get_content_from_research
from .utils.scripter_utils import prepare_scripter_configs
import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Orchestrator:
    def __init__(self):
        self.research_service = ResearchService()
        self.scripter_service = ScripterService()
        self.tts_service = TTSService()

    
    async def run_research_service(self):
        research_input = prepare_input_for_research(self.request_dict)
        research_output = await self.research_service.run(**research_input)
        return research_output
    

    async def run_scripter_service(self, content):
        scripter_input = prepare_scripter_configs(self.request_dict, content)
        scripter_output = await self.scripter_service.run(**scripter_input)
        return scripter_output
        

    async def generate_podcast(self, request: PodcasterInput):
        try:
            logger.info(f"Received request for topic: {request.topic} and mode: {request.scraper_mode}")
            self.request_dict = convert_input_to_dict(request)
            research_output = await self.run_research_service()
            content = get_content_from_research(research_output)
            scripter_output = await self.run_scripter_service(content)
            

    
        except Exception as e:
            logger.error(f"Error in Research Service: {e}")
            raise e



