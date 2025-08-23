from fastapi import FastAPI, Query
from .request_model import TTSInput
from .handler import generate_text_to_speech

app = FastAPI(title="TTS - Text to Speech API")
 # Optionally pass llama_index

@app.post("/tts")
async def generate_research(request: TTSInput):
    return generate_text_to_speech(request.prompt, request.config, request.model, request.speaker_config, num_speakers=request.num_speakers)
    
@app.get("/tts_health")
async def health_check():
    return {"status": "ok", "message": "Welcome to TTS API. Version 1.0,  17.08.2025"}


