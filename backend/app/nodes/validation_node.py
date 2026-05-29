def run(state: dict) -> dict:
    missing_info = []
    
    # Check if we need more info based on intent policy
    intent = state.get("intent", "")
    message = state.get("message", "").lower()
    
    if intent == "account_inquiry" and "account" not in message and "balance" not in message:
        missing_info.append("account number")
        
    if intent == "transaction_dispute" and ("amount" not in message and "date" not in message):
        missing_info.append("transaction details (amount, date)")
        
    state["missing_info"] = missing_info
    state["is_valid"] = len(missing_info) == 0
    
    return state
