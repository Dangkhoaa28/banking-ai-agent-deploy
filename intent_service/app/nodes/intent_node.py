import json
import re
from typing import Dict, Any
from app.clients.ollama_client import OllamaClient
from app.core.schemas import IntentResponse

class IntentNode:
    def __init__(self):
        self.ollama_client = OllamaClient()

    def _build_prompt(self, message: str) -> str:
        return f"""You are an advanced banking intent prediction model.
Classify the following customer message into one of these intents:
- account_inquiry
- transaction_dispute
- loan_inquiry
- card_issue
- general_inquiry

Customer Message: "{message}"

Respond ONLY with a JSON object in this exact format, with no markdown formatting or extra text:
{{
    "intent": "predicted_intent",
    "confidence": 0.95,
    "reason": "short explanation of why"
}}
"""

    def predict_intent(self, message: str) -> IntentResponse:
        prompt = self._build_prompt(message)
        response_dict = self.ollama_client.generate_sync(prompt)
        
        if "error" in response_dict:
            return IntentResponse(
                intent="general_inquiry",
                confidence=0.0,
                reason=f"Error connecting to Ollama: {response_dict['error']}"
            )
            
        final_text = response_dict.get("response", "")
        
        # Try to parse the output
        try:
            # Look for JSON block in case Ollama outputted markdown
            json_str = final_text
            json_match = re.search(r'\{.*\}', final_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                
            parsed = json.loads(json_str)
            intent = parsed.get("intent", "general_inquiry")
            confidence = float(parsed.get("confidence", 0.5))
            reason = parsed.get("reason", "No reason provided")
            
            return IntentResponse(intent=intent, confidence=confidence, reason=reason)
            
        except Exception as e:
            # Fallback if parsing fails
            return IntentResponse(
                intent="general_inquiry",
                confidence=0.1,
                reason=f"Failed to parse LLM output: {str(e)}. Raw output: {final_text}"
            )
