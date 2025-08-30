import logging
from .tts.gemini import GeminiTTS
from .request_model import TTSInput  # assuming your pydantic models live in models.py
import app.tts.helper as helper
import app.tts.constant as constant
import traceback
# Logging configuration
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


async def generate_text_to_speech(uid, topic, prompt, content, model_name, model, speaker_config, num_speakers):
    """
    Generate text-to-speech audio from the given TTSInput request.
    """
    output_file_dict = {}
    try:
        logger.info(f"Received TTS request with model={model}")

        # Extract values from request
        if num_speakers not in [1, 2]:
            logger.error(f"Number of speakers must be 1 or 2, but got {num_speakers}")
            raise ValueError(f"Number of speakers must be 1 or 2, but got {num_speakers}")

        if model == "gemini":
            # Get number of speakers from config (count non-empty speaker names)
            
            #speaker_config = helper.get_speaker_config(speaker_config)
            model = model_name
            augmented_prompt = helper.augment_prompt_with_content(prompt, content)
            
            logger.info(f"Using GeminiTTS with {num_speakers} speakers")

            # Initialize GeminiTTS
            gemini_tts = GeminiTTS(num_speakers=num_speakers, model=model)
        
            # Pass the prompt + speaker mapping
            response = await gemini_tts.text_to_speech(
                augmented_prompt,
                speaker_config
            )

            output_filename = helper.get_output_filename(constant.output_dir, uid, topic)
            logger.info(f"Writing output to {output_filename}")
            helper.wave_file(output_filename, response)
            output_file_dict['episode_name'] = topic
            output_file_dict['episode_path'] = output_filename
            return output_file_dict, None

        else:
            logger.error(f"Model {model} not supported yet")
            raise ValueError(f"Model {model} not implemented")

    except Exception as e:
        logger.error(f"Error occurred while generating text-to-speech: {traceback.format_exc(e)}")
        return None, str(e)

