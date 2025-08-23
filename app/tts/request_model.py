from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class TTSModel(str, Enum):
    GEMINI = "gemini"
    MURF = "murf"

class SpeakerConfig(BaseModel):
    speaker_name:str
    speaker_voice:str


class GeminiConfig(BaseModel):
    model_name: str = "gemini-2.5-flash-preview-tts"


class OutputConfig(BaseModel):
    format: str = "mp3"
    merge: bool = True
    background_music: Optional[str] = None


class Config(BaseModel):
    gemini: GeminiConfig = GeminiConfig()
    output: OutputConfig = OutputConfig()


class TTSInput(BaseModel):
    model: TTSModel = TTSModel.GEMINI   # default to Gemini
    config: Config = Config()
    prompt: str 
    num_speakers: Optional[int] = 2
    speaker_config: List[SpeakerConfig]


