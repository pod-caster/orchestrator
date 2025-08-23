import app.scripter.utils.yaml_loader as yaml_loader
from pathlib import Path
Base_DIR = Path(__file__).resolve().parent.parent

# load all configurations from YAML files
CONFIGS_PATH = Base_DIR / "configs"
configs = yaml_loader.load_yaml_files_as_namespace(CONFIGS_PATH)

# Prompt constants
DISCUSSION_CARD_PROMPT = configs.prompt["discussion_card_generator"]
DIALOGUE_PROMPT = configs.prompt["dialogue_generator"]

# LLM Constants
## OpenAI
OPENAI_URL = configs.llm_configs["openai"]["url"]
OPENAI_MODEL = configs.llm_configs["openai"]["model"]
OPENAI_TEMPERATURE = configs.llm_configs["openai"]["temperature"]
OPENAI_CONCURRENCY_LIMIT = 2
OPENAI_API_KEYS = configs.llm_configs["openai"]["api_key"]
## Gemini
GEMINI_URL = configs.llm_configs["gemini"]["url"]
GEMINI_MODEL = configs.llm_configs["gemini"]["model"]
GEMINI_TEMPERATURE = configs.llm_configs["gemini"]["temperature"]
GEMINI_CONCURRENCY_LIMIT = 2
GEMINI_API_KEYS = configs.llm_configs["gemini"]["api_key"]

# Miscellaneous constants
rows_per_key = 1  # Number of rows per API key