from ..tts.handler import generate_text_to_speech
import time
import logging
# Logging configuration
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class TTSService:
    def run(self, prompt, tts_configs, model, speaker_config, num_speakers=2):
        logger.info(f"Running TTS Service with model {model}")
        start = time.time()
        output = generate_text_to_speech(prompt, tts_configs, model, speaker_config, num_speakers)
        end = time.time()
        logger.info(f"TTS Service completed in {round(end - start, 2)} seconds")   
        return output