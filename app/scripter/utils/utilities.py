import pandas as pd
import json
import logging
import re
import ast

import app.scripter.utils.constant as constant

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def assign_api_keys_to_rows(df,llm_provider):
    if llm_provider == 'openai':
        apikeys = constant.OPENAI_API_KEYS
    else:
        apikeys = constant.GEMINI_API_KEYS
    repeated_list = [item for item in apikeys for _ in range(constant.rows_per_key)]
    repeated_list_expanded = (repeated_list * ((len(df) // len(repeated_list)) + 1))[:len(df)]
    df['api_keys'] = repeated_list_expanded
    return df

# def llm_response_parser(data,llm_provider):
#     try:
#         if llm_provider == 'openai':
#             return json.loads(data.get('choices')[0].get('message').get('content').replace('\n','').replace('json','').replace('`',''))
#         else :
#             if isinstance(data, list):
#                 data = data[0]
#             return json.loads(data['candidates'][0]['content']['parts'][0]['text'].replace('\n','').replace('json','').replace('`',''))
#     except:
#         return None

def llm_response_parser(data, llm_provider):
    """
    Parse JSON output from different LLM providers with error handling
    and automatic sanitization of common formatting issues.
    """

    def extract_raw_text(data, llm_provider):
        """Extract raw text from LLM response depending on provider."""
        if llm_provider == 'openai':
            return data.get('choices', [{}])[0].get('message', {}).get('content', '')
        else:
            if isinstance(data, list):
                data = data[0]
            return data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')

    def sanitize(text: str) -> str:
        """Clean common LLM formatting artifacts before json.loads."""
        text = text.strip()
        # remove markdown fences
        text = text.replace("```json", "").replace("```", "")
        # remove stray newlines and backticks
        text = text.replace("\n", " ").replace("`", "")
        # fix trailing commas inside objects/arrays
        text = re.sub(r",\s*([}\]])", r"\1", text)
        return text

    raw_text = extract_raw_text(data, llm_provider)
    cleaned = sanitize(raw_text)

    # --- Attempt 1: direct JSON parse ---
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e1:
        # --- Attempt 2: escape bad inner quotes ---
        try:
            fixed = re.sub(r'(?<!\\)"(.*?)"(?![:,}])',
                           lambda m: '"' + m.group(1).replace('"', '\\"') + '"',
                           cleaned)
            return json.loads(fixed)
        except json.JSONDecodeError as e2:
            # --- Attempt 3: try Python-safe eval ---
            try:
                return ast.literal_eval(cleaned)
            except Exception as e3:
                # --- All attempts failed ---
                logger.error("JSON parsing failed.")
                logger.error("Raw text: %s", raw_text[:200])
                logger.error("Errors: %s | %s | %s", e1, e2, e3)
                return None

    
def estimate_card_minutes(card):
    if not isinstance(card, dict):
        return 0
    words = len(card.get("summary", "").split()) + len(card.get("context", "").split())
    return words / 150  # 150 words per minute average

def adjust_episode_count(total_duration, target_episodes, min_length):
    episode_count = target_episodes
    while episode_count > 1 and (total_duration / episode_count) < min_length:
        episode_count -= 1
    return episode_count