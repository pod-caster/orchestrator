from typing import List, Literal, Optional
from pydantic import BaseModel, HttpUrl, Field


class UserContent(BaseModel):
    content: List[str] = Field(default_factory=list)
    links: List[HttpUrl] = Field(default_factory=list)


class EpisodeConfigs(BaseModel):
    episode_count: int = Field(..., gt=0, description="Number of episodes to generate")
    min_episode_length: int = Field(..., gt=0, description="Minimum length of each episode in minutes")
    tone: str

class SpeakerDetails(BaseModel):
    speaker_name: str
    speaker_voice: str
    speaker_tone: str

class PodcasterInput(BaseModel):
    topic: str
    scraper_mode: Literal["user", "researcher"]
    user_content: Optional[UserContent] = None
    episode_configs: EpisodeConfigs
    speaker_details: List[SpeakerDetails]



