from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.schemas import AgentRequest, AgentResponse
from app.core.settings import settings
from app.agent.orchestrator import run_workflow

app = FastAPI(title="Banking AI Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "banking-agent"}

@app.get("/config")
def get_config():
    return {
        "intent_host": settings.INTENT_SERVICE_HOST,
        "intent_port": settings.INTENT_SERVICE_PORT,
        "ollama_host": settings.OLLAMA_HOST,
        "ollama_model": settings.OLLAMA_MODEL
    }

@app.post("/run-agent", response_model=AgentResponse)
def run_agent(request: AgentRequest):
    try:
        result = run_workflow(request.message, request.customer_id)
        if result.get("error"):
            # Depending on requirements, we can still return a 200 with partial info
            # but setting the draft reply to the error.
            pass 
        return AgentResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
