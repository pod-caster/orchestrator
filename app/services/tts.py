import asyncio
import time
import logging

# Logging configuration
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from ..tts.handler import generate_text_to_speech

class TTSService:
    async def run(self, uid, topic, script, prompt, model_name, model, speaker_config, num_speakers=2):
        logger.info(f"Running TTS Service with model {model}")
        start = time.time()
        output, error = await generate_text_to_speech(
            uid, topic, prompt, script, model_name, model, speaker_config, num_speakers
        )
        end = time.time()
        logger.info(f"TTS Service completed in {round(end - start, 2)} seconds")
        return output


class TTSRunner:
    def __init__(self, tts_service, max_concurrent: int = 5):
        self.tts_service = tts_service
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def worker(self, tts_input: dict):
        async with self.semaphore:
            # run() is async → await it directly
            return await self.tts_service.run(**tts_input)

    async def run_all(self, tts_inputs: list[dict]):
        tasks = [asyncio.create_task(self.worker(inp)) for inp in tts_inputs]
        output = await asyncio.gather(*tasks, return_exceptions=True)
        output_filtered = [o for o in output if o is not None]
        return output_filtered
