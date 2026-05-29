from pydantic import BaseModel

class IntentRequest(BaseModel):
    message: str

class IntentResponse(BaseModel):
    intent: str
    confidence: float
    reason: str
