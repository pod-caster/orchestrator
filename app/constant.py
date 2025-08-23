from app.utils.helper import load_yaml
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config" / "config.yaml"
RESEARCH_CONFIG_PATH = BASE_DIR / "config" / "research_config.yaml"



config = load_yaml(CONFIG_PATH)
research_config = load_yaml(RESEARCH_CONFIG_PATH).get("research_configs", {})