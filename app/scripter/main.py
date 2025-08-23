from fastapi import FastAPI, Query
from pydantic import BaseModel
import handler
import asyncio
import uvicorn

app = FastAPI(title="AI Podcast Generator - Script API")

MAX_CONCURRENT_REQUESTS = 3
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

class TopicRequest(BaseModel):
    topic: str
    script_configs: dict
    content: list
    
@app.post("/script_writer")
async def generate_script(request: TopicRequest):
    async with semaphore:
        result = await handler.main_function(request.topic,request.script_configs, request.content)
    return {"script_output": result}

@app.get("/script_health")
async def health_check():
    return {"status": "ok", "message": "Welcome to AI Podcast Generator Script API. Version 3.0,  21.08.2025"}

if __name__ == '__main__':
    uvicorn.run(app, port=8000, log_level='info')

