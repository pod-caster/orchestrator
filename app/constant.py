from app.utils.helper import load_yaml
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config" / "config.yaml"
RESEARCH_CONFIG_PATH = BASE_DIR / "config" / "research_config.yaml"
SCRIPTER_CONFIG_PATH = BASE_DIR / "config" / "scripter_config.yaml"
TTS_CONFIG_PATH = BASE_DIR / "config" / "tts.yaml"



config = load_yaml(CONFIG_PATH)
research_config = load_yaml(RESEARCH_CONFIG_PATH).get("research_configs", {})
scripter_configs = load_yaml(SCRIPTER_CONFIG_PATH).get("scripter", {})
tts_config = load_yaml(TTS_CONFIG_PATH).get("tts", {})