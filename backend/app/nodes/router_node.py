def run(state: dict) -> dict:
    confidence = state.get("confidence", 0.0)
    
    if confidence < 0.5:
        state["route"] = "clarification"
    else:
        state["route"] = "continue"
        
    return state
