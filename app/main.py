from fastapi import FastAPI
from app.model.request_model import PodcasterInput
from app.handler import Orchestrator
import logging
# Logging configuration
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')   
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = FastAPI(title="Orchestrator API")


@app.post("/generate_podcast")
async def generate_podcast(request: PodcasterInput):
    orchestrator = Orchestrator()
    return await orchestrator.generate_podcast(request)
    
@app.get("/tts_health")
async def health_check():
    return {"status": "ok", "message": "Orchestrator API is Healthy", "version":"1.0"}


