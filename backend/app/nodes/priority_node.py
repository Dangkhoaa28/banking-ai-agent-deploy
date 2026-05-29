def run(state: dict) -> dict:
    intent = state.get("intent", "general_inquiry")
    
    # Priority logic
    if intent in ["transaction_dispute", "card_issue"]:
        priority = "HIGH"
    elif intent in ["loan_inquiry"]:
        priority = "MEDIUM"
    else:
        priority = "LOW"
        
    state["priority"] = priority
    return state
