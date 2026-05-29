from pydantic import BaseModel
from typing import Optional, List

class AgentRequest(BaseModel):
    message: str
    customer_id: Optional[str] = None

class AgentResponse(BaseModel):
    intent: str
    confidence: float
    priority: str
    policy: str
    draft_reply: str
    missing_info: List[str]
    next_action: str
    processing_time: float
