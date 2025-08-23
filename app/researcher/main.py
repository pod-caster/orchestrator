from fastapi import FastAPI, Query
from pydantic import BaseModel
from .research.research_agent import ResearchAgent
import extract

app = FastAPI(title="AI Podcast Generator - Research API")

agent = ResearchAgent()  # Optionally pass llama_index

class TopicRequest(BaseModel):
    topic: str
    research_configs: dict 
    
@app.post("/research")
async def generate_research(request: TopicRequest):
    result = await extract.extract(request.topic,request.research_configs)
    return result

@app.get("/research_health")
async def health_check():
    return {"status": "ok", "message": "Welcome to AI Podcast Generator Research API. Version 1.2,  17.05.2025"}
