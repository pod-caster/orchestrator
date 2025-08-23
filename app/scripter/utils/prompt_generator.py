import pandas as pd

import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import app.scripter.utils.constant as constant

def generate_discussion_card_prompt(topic: str,link: str, content: str) -> str:
    """
    Generate a prompt for discussion cards based on the topic and content.
    
    Args:
        topic (str): The topic for which the discussion card is generated.
        content (str): The content to be used in the discussion card.
    
    Returns:
        str: The generated prompt for discussion cards.
    """
    # Example implementation of prompt generation
    return constant.DISCUSSION_CARD_PROMPT.replace("<TOPIC>", topic).replace("<CONTEXT>", content).replace("<LINK>", link)

def generate_dialogue_prompt(episode_title: str, episode: str, episode_length: str, number_speakers: str, speaker_details: str, tone_description: str) -> str:
    """
    Generate a prompt for dialogue based on the episode title, speakers, and dialogue content.

    Args:
        episode_title (str): The title of the episode.
        speakers (list): A list of speakers in the episode.
        dialogue (str): The dialogue content to be used in the prompt.

    Returns:
        str: The generated prompt for dialogue.
    """
    # Example implementation of prompt generation
    return constant.DIALOGUE_PROMPT.replace("<EPISODE_TITLE>", episode_title).replace("<EPISODE>", episode).replace("<EPISODE_LENGTH>", episode_length).replace("<NUM_SPEAKERS>", number_speakers).replace("<SPEAKER_DETAILS>", speaker_details).replace("<TONE_DESCRIPTION>", tone_description)