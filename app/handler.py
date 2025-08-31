from .services.researcher import ResearchService
from .services.scripter import ScripterService
from .services.tts import TTSService, TTSRunner
from .model.request_model import PodcasterInput
from .utils.helper import convert_input_to_dict, get_unique_id, prepare_output_json
from .utils.research_utils import prepare_input_for_research, get_content_from_research
from .utils.scripter_utils import prepare_scripter_configs
from .utils.tts_utils import prepare_tts_input
import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Orchestrator:
    def __init__(self):
        self.research_service = ResearchService()
        self.scripter_service = ScripterService()
        self.tts_service = TTSService()

    def set_var(self, var_name, var_value):
        setattr(self, var_name, var_value)

    
    async def run_research_service(self):
        research_output = {}
        user_content = []
        research_input, user_content, to_use_research  = prepare_input_for_research(self.request_dict)
        self.set_var('to_use_research', to_use_research)
        if not to_use_research:
            logger.info("Skipping research service as user provided content without links.")
            return research_output, user_content
        else:
            research_output = await self.research_service.run(**research_input)
            return research_output, user_content
    

    async def run_scripter_service(self, content):
        scripter_input = prepare_scripter_configs(self.request_dict, content)
        scripter_output = await self.scripter_service.run(**scripter_input)
        return scripter_output
        

    async def run_tts_service(self, script_output):
        # Prepare list of dicts
        tts_input_list = prepare_tts_input(
            script_output.get('dialogues', []),
            self.request_dict.get("speaker_details", [])
        )

        # Create runner with concurrency limit (say 5 workers)
        runner = TTSRunner(self.tts_service, max_concurrent=5)

        # Run all TTS calls concurrently
        tts_output_path_list = await runner.run_all(tts_input_list)

        return tts_output_path_list

    async def generate_podcast(self, request: PodcasterInput):
        
        try:
            tts_output_path_lists = []
            logger.info(f"Received request for topic: {request.topic} and mode: {request.scraper_mode}")
            self.request_dict = convert_input_to_dict(request)
            research_output, user_content = await self.run_research_service()
            
            content = get_content_from_research(research_output, user_provided_content = user_content)
            scripter_output = await self.run_scripter_service(content)

            tts_output_path_lists = await self.run_tts_service(scripter_output)

            output_json = prepare_output_json(tts_output_path_lists)
            return output_json


        except Exception as e:
            output_json = prepare_output_json(tts_output_path_lists, error_message=str(e))
            logger.error(f"Error in podcast generation: {e}")
            return output_json



