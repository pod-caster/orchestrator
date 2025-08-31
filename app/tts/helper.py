import wave
import json
import logging
import re
import os

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
   

def augment_prompt_with_content(prompt, content, delimiter = "\n\nHere is the content:\n"):
   try:
      if not content or len(content.strip()) == 0:
         raise ValueError("Content is empty")
      augmented_prompt = f"{prompt}{delimiter}{content}"
      return augmented_prompt
   
   except Exception as e:
      logger.error(f"Error occured while augmenting prompt with content {str(e)}")
      raise e
   

def get_output_filename(output_dir, uid, topic, filetype="wav"):
    if not isinstance(uid, str):
        uid = str(uid)
    
    # Replace spaces with underscores
    safe_topic = topic.replace(" ", "_")
    
    # Remove/replace characters not allowed in filenames
    safe_topic = re.sub(r'[\\/*?:"<>|]', "_", safe_topic)
    
    # Construct path safely
    filename = f"{uid}_{safe_topic}.{filetype}"
    return os.path.join(output_dir, filename)