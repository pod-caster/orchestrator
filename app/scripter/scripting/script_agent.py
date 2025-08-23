import pandas as pd

import logging
logging.basicConfig(format = '%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from ..scripting.discussion_card_generator import DiscussCardGenerator
from ..scripting.episode_generator import EpisodeGenerator
from ..scripting.dialogue_generator import DialogueGenerator

class SciptAgent:
    def __init__(self, topic: str, script_flags: dict, content: pd.DataFrame):
        self.topic = topic
        self.script_flags = script_flags
        self.content = content
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    async def run_scripter(self):
        self.logger.info(f"Running script agent for topic: {self.topic}")
        dis_cards = DiscussCardGenerator(self.topic, self.content, self.script_flags.get('dicussion_card_configs', {}))
        # Generate discussion cards
        discussion_cards = await dis_cards.generate_discussion_card()
        # Group discussion cards into episodes
        episodes = EpisodeGenerator(discussion_cards, self.script_flags.get('episode_configs', {}))
        episode_lists, episode_count, total_duration = await episodes.group_cards_by_episode_count()
        # Generate dialogues
        dialogue_generator = DialogueGenerator(episode_lists, self.script_flags.get('dialogue_configs', {}))
        dialogues = await dialogue_generator.generate_dialogue()
        return { "discussion_cards": discussion_cards , "episodes": episode_lists, "episode_count": episode_count, "total_duration": total_duration, "dialogues": dialogues }