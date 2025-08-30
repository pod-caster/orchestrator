import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
import app.constant as constant
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def prepare_speaker_configs_for_scripter(speaker_configs):
    speaker_configs_scripter = {}
    guest_key = "Guest"
    count = 1
    for item in speaker_configs:
        is_host = item.get("is_host", False)
        if is_host:
            speaker_key = "Host"
            speaker_name = item.get("speaker_name", "Host")
            speaker_configs_scripter[speaker_key] = speaker_name
            continue

        else:
            speaker_key = f"{guest_key}{count}"
            speaker_name = item.get("speaker_name", f"Guest{count}")
            speaker_configs_scripter[speaker_key] = speaker_name
            count += 1
    return speaker_configs_scripter
        
def prepare_scripter_configs(input_dict, content):
    final_config = {}
    input_dict = input_dict.copy()
    run_time_scripter_configs = {}
    run_time_dialogue_configs = {}
    topic = input_dict.get("topic", None)
    
    if len(content) == 0:
        raise ValueError("Content is required for scripter service.")
    if not topic:
        raise ValueError("Topic is required for scripter service.")
    
    episode_configs = input_dict.get("episode_configs", {})
    speaker_configs = input_dict.get("speaker_details", [])
    speaker_configs_for_scripter = prepare_speaker_configs_for_scripter(speaker_configs)
    speaker_count = len(speaker_configs)

    if speaker_count == 0:
        raise ValueError("At least one speaker configuration is required.")
    
    if len(episode_configs) == 0:
        raise ValueError("Episode configurations are required for scripter service.")
    
    scripter_default_configs = constant.scripter_configs['script_configs'].copy()
    run_time_scripter_configs['entity_count'] = speaker_count
    scripter_default_configs.update(episode_configs)
    run_time_dialogue_configs['speaker_count'] = speaker_count
    run_time_dialogue_configs['script_tone'] = episode_configs['tone']
    run_time_dialogue_configs['speaker_details'] = speaker_configs_for_scripter
    scripter_default_configs['dialogue_configs'].update(run_time_dialogue_configs)
    scripter_default_configs.update(run_time_scripter_configs)
    del episode_configs['tone']
    final_config['topic'] = topic
    final_config['extracted_content'] = content
    final_config['script_configs'] = scripter_default_configs
    return final_config

