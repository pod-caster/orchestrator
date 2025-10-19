from pydantic_settings import BaseSettings
from pathlib import Path
Base_DIR = Path(__file__).resolve().parent.parent.parent
env_file_path = Base_DIR / ".env"

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    OPENAI_API_KEY: str

    class Config:
        env_file = str(env_file_path) # automatically loads from .env

settings = Settings()
