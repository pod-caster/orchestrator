import wave
import json
import logging

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
   with wave.open(filename, "wb") as wf:
      wf.setnchannels(channels)
      wf.setsampwidth(sample_width)
      wf.setframerate(rate)
      wf.writeframes(pcm)

   
def get_speaker_config(speaker_config):
   try:
      if len(speaker_config) == 0:
         raise ValueError("speaker_config is empty")
      final = [item.model_dump() for item in speaker_config]
      return final
   
   except Exception as e:
      logger.error(f"Error occured while preparing speaker config {str(e)}")
      return {}