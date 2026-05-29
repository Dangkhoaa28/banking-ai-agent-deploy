import time
from typing import Dict, Any
import logging

from app.nodes import (
    intent_node, 
    priority_node, 
    policy_node, 
    router_node, 
    validation_node, 
    draft_node
)

def run_workflow(message: str, customer_id: str = None) -> Dict[str, Any]:
    start_time = time.time()
    
    state = {
        "message": message,
        "customer_id": customer_id,
        "intent": "",
        "confidence": 0.0,
        "reason": "",
        "priority": "",          
        "policy": "",
        "route": "",
        "is_valid": False,
        "missing_info": [],
        "draft_reply": "",
        "next_action": "",
        "error": None,
    }
    
    try:
        # Sequential workflow
        state = intent_node.run(state)
        
        if state.get("error"):
            # Early exit if parsing fails totally, though intent node should handle basic fallback
            return format_response(state, start_time)
            
        state = priority_node.run(state)
        state = policy_node.run(state)
        state = router_node.run(state)
        state = validation_node.run(state)
        state = draft_node.run(state)
        
    except Exception as e:
        logging.error(f"Workflow error: {str(e)}")
        state["error"] = str(e)
        
    return format_response(state, start_time)

def format_response(state: dict, start_time: float) -> dict:
    return {
        "intent": state.get("intent", "error"),
        "confidence": state.get("confidence", 0.0),
        "priority": state.get("priority", "UNKNOWN"),
        "policy": state.get("policy", "Error processing policy."),
        "draft_reply": state.get("draft_reply", "Sorry, an error occurred while processing your request."),
        "missing_info": state.get("missing_info", []),
        "next_action": state.get("next_action", "error"),
        "processing_time": round(time.time() - start_time, 2)
    }
