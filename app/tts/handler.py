import logging
from .tts.gemini import GeminiTTS
from .request_model import TTSInput  # assuming your pydantic models live in models.py
import app.tts.helper as helper
# Logging configuration
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def generate_text_to_speech(prompt, config, model, speaker_config, num_speakers=2):
    """
    Generate text-to-speech audio from the given TTSInput request.
    """

    logger.info(f"Received TTS request with model={model}")

    # Extract values from request
    if num_speakers not in [1, 2]:
        logger.error(f"Number of speakers must be 1 or 2, but got {num_speakers}")
        raise ValueError(f"Number of speakers must be 1 or 2, but got {num_speakers}")

    if model == "gemini":
        # Get number of speakers from config (count non-empty speaker names)
        
        speaker_config = helper.get_speaker_config(speaker_config)
        model = config.gemini.model_name
        
        
        logger.info(f"Using GeminiTTS with {num_speakers} speakers")

        # Initialize GeminiTTS
        gemini_tts = GeminiTTS(num_speakers=num_speakers, model=model)
        
        # Pass the prompt + speaker mapping
        response = gemini_tts.text_to_speech(
            prompt,
            speaker_config
        )


        helper.wave_file("output.wav", response)

    else:
        logger.error(f"Model {model} not supported yet")
        raise ValueError(f"Model {model} not implemented")


