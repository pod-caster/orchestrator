import pandas as pd
import json

import app.scripter.utils.constant as constant

def assign_api_keys_to_rows(df,llm_provider):
    if llm_provider == 'openai':
        apikeys = constant.OPENAI_API_KEYS
    else:
        apikeys = constant.GEMINI_API_KEYS
    repeated_list = [item for item in apikeys for _ in range(constant.rows_per_key)]
    repeated_list_expanded = (repeated_list * ((len(df) // len(repeated_list)) + 1))[:len(df)]
    df['api_keys'] = repeated_list_expanded
    return df

def llm_response_parser(data,llm_provider):
    try:
        if llm_provider == 'openai':
            return json.loads(data.get('choices')[0].get('message').get('content').replace('\n','').replace('json','').replace('`',''))
        else :
            if isinstance(data, list):
                data = data[0]
            return json.loads(data['candidates'][0]['content']['parts'][0]['text'].replace('\n','').replace('json','').replace('`',''))
    except:
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