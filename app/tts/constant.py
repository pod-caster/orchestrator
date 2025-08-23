from .settings import settings

GEMINI_API_KEY = settings.GEMINI_API_KEY
gemini_model = "gemini-2.5-flash-preview-tts"


gemini_speaker1_default_voice = "Schedar"
gemini_speaker2_default_voice = "Puck"


default_speaker1_config = {"voice": gemini_speaker1_default_voice}
default_speaker2_config = {"voice": gemini_speaker2_default_voice}