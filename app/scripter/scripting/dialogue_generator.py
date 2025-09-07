import pandas as pd

import logging
logging.basicConfig(format = '%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import app.scripter.utils.prompt_generator as prompter
import app.scripter.utils.utilities as utils
import app.scripter.utils.call_llms as llm_caller


class DialogueGenerator:
    def __init__(self,episode_list: list, dialogue_configs: dict):
        self.episode_list = episode_list
        self.llm_provider = dialogue_configs.get('llm_provider', 'gemini')
        self.speaker_count = dialogue_configs.get('speaker_count', 2)
        self.script_tone = dialogue_configs.get('script_tone', 'informal')
        self.speaker_details = dialogue_configs.get('speaker_details', [])

    async def generate_dialogue(self):
        logger.info("Generating dialogue for episodes")
        ## Get llm provider from discuss_configs, default to gemini
        episode_df = pd.DataFrame(self.episode_list)

        ## Convert list of episodes into a dataframe
        episode_df["estimated_minutes"] = episode_df["estimated_minutes"].apply(
            lambda x: f"{int(x*60)//60} min{'s' if int(x*60)//60 != 1 else ''} "
                    f"{int(x*60)%60} sec{'s' if int(x*60)%60 != 1 else ''}"
        )
        ## Generate prompts for discussion cards
        logger.info("Generating prompts for discussion cards")
        episode_df['prompt'] = episode_df.apply(
            lambda row: prompter.generate_dialogue_prompt(str(row['episode_title']), str(row['cards']), str(row['estimated_minutes']), str(self.speaker_count), str(self.speaker_details), self.script_tone),
            axis=1
        )

        ## assign api keys to each row based on llm provider
        logger.info("Assign API keys for prompts")
        episode_df = utils.assign_api_keys_to_rows(episode_df, self.llm_provider)

        ## call llm for each content parallely
        prompt_list = list(zip(episode_df['prompt'], episode_df['api_keys']))
        response_data = await llm_caller.call_llms(prompt_list,self.llm_provider)

        ## parse llm response and create Dialogue objects
        logger.info("Parsing LLM responses and creating dialogues")
        dialogues = [utils.llm_response_parser(i,self.llm_provider) for i in response_data]
        dialogues = [item for item in dialogues if item is not None and item==item]
        if len(dialogues) == 0:
            raise ValueError("No valid dialogues generated from LLM responses.")
        dialogues = [{**ep, "script": "\n".join(f"{d['speaker']} - {d['text']}" for d in ep["script"])} for ep in dialogues]
        dialogues = [{**d, "script_tone": self.script_tone, "speaker_details": self.speaker_details} for d in dialogues]
        
        # return dialogues
        return dialogues

if __name__ == "__main__":
    # Example usage

    dialogue_configs = {
    }
    
    agent = DialogueGenerator(dialogue_configs)
