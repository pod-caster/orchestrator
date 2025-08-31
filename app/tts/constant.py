from .settings import settings
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


GEMINI_API_KEY = settings.GEMINI_API_KEY
gemini_model = "gemini-2.5-flash-preview-tts"


gemini_speaker1_default_voice = "Schedar"
gemini_speaker2_default_voice = "Puck"


default_speaker1_config = {"voice": gemini_speaker1_default_voice}
default_speaker2_config = {"voice": gemini_speaker2_default_voice}

output_dir = f"{BASE_DIR}/output"

if not output_dir.exists():
    output_dir.mkdir(parents=True, exist_ok=True)

