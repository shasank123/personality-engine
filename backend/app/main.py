from fastapi import FastAPI, HTTPException
from .models import MemoryProfile, ChatLogInput, ChatRequest, PersonalityResponse
from .services import LLMService

app = FastAPI(title="Personality Engine API")

@app.get("/")
def health_check():
    return {"status": "active", "version": 1.0}

@app.post("/extract-memory", response_model=MemoryProfile)
def extract_memory_endpoint(data: ChatLogInput):
    """
    Analyzes raw chat logs and returns a structural profile.
    """

    if not data.messages.strip():
        raise HTTPException(status_code=400, detail="Chat logs cannot be empty.")
    
    memory = LLMService.extract_memory(data.messages)
    return memory

@app.post("/chat", response_model=PersonalityResponse)
def chat_endpoint(data: ChatRequest):
    """
    Returns both the raw AI response and the personality-infused response.
    """
    before, after = LLMService.generate_response(
        data.user_query,
        data.memory_context,
        data.persona
    )
    
    return PersonalityResponse(
        original_response=before,
        personalized_response=after,
        applied_tone=data.persona
    )
    