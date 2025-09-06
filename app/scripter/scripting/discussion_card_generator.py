import logging
logging.basicConfig(format = '%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import app.scripter.utils.prompt_generator as prompter
import app.scripter.utils.utilities as utils
import app.scripter.utils.call_llms as llm_caller

class DiscussCardGenerator:
    def __init__(self,topic: str, content: str, discuss_configs: dict ):
        self.topic = topic
        self.content = content
        self.discuss_configs = discuss_configs

    async def generate_discussion_card(self):
        logger.info(f"Generating discussion card for topic: {self.topic}")
        ## Get llm provider from discuss_configs, default to gemini
        llm_provider = self.discuss_configs.get('llm_provider', 'gemini')
        
        ## Generate prompts for discussion cards
        logger.info("Generating prompts for discussion cards")
        self.content['prompt'] = self.content.apply(
            lambda row: prompter.generate_discussion_card_prompt(self.topic,row['link'], row['content']),
            axis=1
        )
        
        ## assign api keys to each row based on llm provider
        logger.info("Assign API keys for prompts")
        self.content = utils.assign_api_keys_to_rows(self.content, llm_provider)
               
        ## call llm for each content parallely
        prompt_list = list(zip(self.content['prompt'], self.content['api_keys']))
        response_data = await llm_caller.call_llms(prompt_list,llm_provider)
        
        ## parse llm response and create DiscussCard objects
        logger.info("Parsing LLM responses and creating discussion cards")
        
        discussion_cards = [utils.llm_response_parser(i,llm_provider) for i in response_data]
        discussion_cards = [item for item in discussion_cards if item is not None]
        if len(discussion_cards) == 0:
            raise ValueError("No valid discussion cards generated from LLM responses.")
        ## Return a list of DiscussCard objects
        # return [DiscussCardGenerator(**card) for card in discussion_cards]  # Filter out empty responses
        return [item for sublist in discussion_cards for item in sublist]


if __name__ == "__main__":
    # Example usage
    link = "https://www.example.com"
    link_id = "url1"
    content = "This is a sample content for the script agent."
    discuss_configs = {
    }
    
    agent = DiscussCardGenerator(link,content, link_id, discuss_configs)
    print(agent.content)


