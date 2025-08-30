import logging
import app.constant as constant
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
import random
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def prepare_single_input_for_tts(tts_provider, speaker_details, model_name, topic, prompt, content, id):
    final_input = {}
    if len(content) == 0:
        raise ValueError("Script is required for TTS service.")
    if not topic:
        raise ValueError("Topic is required for TTS service.")

    final_input['uid'] = id
    final_input['topic'] = topic
    final_input['prompt'] = prompt
    final_input['script'] = content
    final_input['model_name'] = model_name
    final_input['model'] = tts_provider
    final_input['speaker_config'] = speaker_details
    final_input['num_speakers'] = len(speaker_details)
    return final_input

def generate_tts_prompt(prompt, episode_title, overall_tone, speaker_details):
    if len(speaker_details) == 0:
        raise ValueError("Speaker details are required to generate TTS prompt.")
    speaker_tone_dict = str({speaker["speaker_name"]: speaker["speaker_tone"] for speaker in speaker_details})
    return prompt.format(
        episode_title=episode_title,
        overall_tone=overall_tone,
        speaker_tones=speaker_tone_dict
    )


def prepare_tts_input(script_output_dict, speaker_details):
    tts_inputs = []
    tts_provider = constant.config.get('tts_provider', 'gemini')
    prompt = constant.tts_config[tts_provider]['prompt']
    model = constant.tts_config[tts_provider]['model_name']
    
    if len(script_output_dict) == 0:
        raise ValueError("Script output is empty, cannot prepare TTS input.")
    for item in script_output_dict:
        try:    
            ep_title = item.get("episode_title", "default_topic")
            content = item.get("script", "")
            tone = item.get("script_tone", "neutral")
            if len(content) == 0:
                logger.warning(f"Script content is empty for topic {ep_title}, skipping TTS input preparation.")
                continue
            formatted_prompt = generate_tts_prompt(
                prompt,
                episode_title=ep_title,
                overall_tone=tone,
                speaker_details=speaker_details
            )
            tts_input = prepare_single_input_for_tts(
                tts_provider=tts_provider,
                model_name=model,
                speaker_details=speaker_details,
                topic=ep_title,
                prompt=formatted_prompt,
                content=content,
                id=random.randint(1000, 9999)
            )
            tts_inputs.append(tts_input)
        except Exception as e:
            logger.error(f"Error preparing TTS input for episode {ep_title}: {e}")
            continue

    return tts_inputs
