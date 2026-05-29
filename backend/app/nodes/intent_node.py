from app.clients.grpc_intent_client import GrpcIntentClient

def run(state: dict) -> dict:
    client = GrpcIntentClient()
    result = client.predict_intent(state["message"])
    
    state["intent"] = result["intent"]
    state["confidence"] = result["confidence"]
    state["reason"] = result["reason"]
    
    if result.get("error"):
        state["error"] = result["error"]
        
    return state
