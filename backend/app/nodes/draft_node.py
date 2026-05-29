import json
import asyncio
from app.clients.ollama_client import OllamaClient

def run_sync(state: dict) -> dict:
    # Need to run async client in a synchronous loop for the orchestrator if it's sync
    # Or just use httpx sync client inside. We'll run the async method nicely.
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    return loop.run_until_complete(run_async(state))
    

async def run_async(state: dict) -> dict:
    if state.get("route") == "clarification":
        state["draft_reply"] = "I'm not quite sure I understood. Could you please provide more clarification on your request?"
        state["next_action"] = "wait_for_customer"
        return state
        
    client = OllamaClient()
    
    message = state.get("message", "")
    intent = state.get("intent", "")
    priority = state.get("priority", "")
    policy = state.get("policy", "")
    missing_info = state.get("missing_info", [])
    
    missing_text = ", ".join(missing_info) if missing_info else "None"
    
    prompt = f"""You are a professional banking AI agent assistant.
Your task is to draft a reply to the customer's message.

Customer Message: "{message}"
Intent: {intent}
Priority Level: {priority}
Bank Policy for this intent: "{policy}"
Missing Information from customer: {missing_text}

Draft a courteous, helpful reply enforcing the bank policy. 
If there is missing information, ask for it politely.

Return ONLY a valid JSON string (no markdown ticks) in this exact format:
{{
    "reply": "your drafted message here",
    "next_action": "e.g., wait_for_info, route_to_human, resolve"
}}
"""
    
    response_dict = await client.generate_async(prompt)
    if "error" in response_dict:
        state["draft_reply"] = f"System Error: {response_dict['error']}"
        state["next_action"] = "system_error"
        return state
        
    final_text = response_dict.get("response", "{}")
    
    try:
        if "{" in final_text:
            json_str = final_text[final_text.find("{"):final_text.rfind("}")+1]
        else:
            json_str = "{}"
            
        parsed = json.loads(json_str)
        state["draft_reply"] = parsed.get("reply", final_text)
        state["next_action"] = parsed.get("next_action", "unknown")
    except:
        state["draft_reply"] = final_text
        state["next_action"] = "manual_review"
        
    return state

# By default, export a generic run
def run(state: dict) -> dict:
    return run_sync(state)
