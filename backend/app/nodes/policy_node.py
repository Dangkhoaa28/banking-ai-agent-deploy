from app.data.policies import get_policy

def run(state: dict) -> dict:
    intent = state.get("intent", "")
    state["policy"] = get_policy(intent)
    return state
