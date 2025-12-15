from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# --- Input Models ---
class ChatLogInput(BaseModel):
    messages: str = Field(..., min_length=50, description="Raw chat log text")

class ChatRequest(BaseModel):
    user_query: str
    memory_context: Dict
    persona: str
    include_reasoning: bool = True

# --- Output Models ---:
class MemoryProfile(BaseModel):
    user_preferences: List[str]
    emotional_patterns: List[str]
    facts: Dict[str, str]

class PersonalityResponse(BaseModel):
    original_response: str
    personalized_response: str
    applied_tone: str
    




