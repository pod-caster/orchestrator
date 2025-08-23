from google import genai
from google.genai import types
import logging
import app.tts.constant as constant
import traceback

# Logging configuration
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class GeminiTTS():
    def __init__(self, num_speakers = 2, model = "gemini-2.5-flash-preview-tts"):
        self.client = genai.Client(api_key=constant.GEMINI_API_KEY)
        self.num_speakers = num_speakers
        self.model = model
        self.logger = logger

    def generate_two_speaker_audio(self, prompt, speaker1_config, speaker2_config):
        try:
            self.logger.info(f"Generating multi speaker speech")
            speaker1_name = speaker1_config["speaker_name"]
            speaker1_voice = speaker1_config["speaker_voice"]

            speaker2_name = speaker2_config["speaker_name"]
            speaker2_voice = speaker2_config["speaker_voice"]
            
            response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                        speaker_voice_configs=[
                        types.SpeakerVoiceConfig(
                            speaker=speaker1_name,
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name=speaker1_voice
                                )
                            )
                        ),
                        types.SpeakerVoiceConfig(
                            speaker=speaker2_name,
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name=speaker2_voice
                                )
                            )
                        ),
                        ]
                    )
                )
            )
            )
            return response.candidates[0].content.parts[0].inline_data.data

        except Exception as e:
            self.logger.error(f"Error occurred while generating multi speaker audio: {str(e)}")
            return {}
        
    
    def generate_single_speaker_audio(self, prompt, speaker_config):
        
        try:
            speaker_voice = speaker_config["voice"]

            response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=speaker_voice
                        )
                    )
                )
            )
            )
            return response.candidates[0].content.parts[0].inline_data.data

        except Exception as e:
           self.logger.error(f"Error occurred while generating single speaker audio: {traceback.format_exc(e)}")
           return None
        

    def text_to_speech(self, content, speaker_config):
        if self.num_speakers not in [1, 2]:
            raise Exception(f"Currently our Podcast service does not support more than {self.num_speakers} speakers")
        
        elif self.num_speakers == 2:
            return self.generate_two_speaker_audio(content, speaker_config[0], speaker_config[1])
        
        else:
            return self.generate_single_speaker_audio(content, speaker_config)
        
    
        
    

        

