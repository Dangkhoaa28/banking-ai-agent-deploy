import requests
from typing import Dict, Any
from app.clients.base import BaseClient
from app.core.settings import settings
import asyncio

class OllamaClient(BaseClient):
    def __init__(self):
        self.host = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.api_type = settings.OLLAMA_API_TYPE  # "chat" hoặc "generate"

    def _build_request(self, prompt: str):
        if self.api_type == "chat":
            url = f"{self.host}/api/chat"
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            }
        else:
            url = f"{self.host}/api/generate"
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        return url, payload

    def _extract_response(self, data: dict) -> dict:
        if self.api_type == "chat":
            content = data.get("message", {}).get("content", "")
            return {"response": content}
        return data

    def generate_sync(self, prompt: str) -> Dict[str, Any]:
        url, payload = self._build_request(prompt)
        try:
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            return self._extract_response(response.json())
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}

    async def generate_async(self, prompt: str) -> Dict[str, Any]:
        # Offload sinh request đồng bộ chạy trên thread riêng tránh khóa ev loop
        return await asyncio.to_thread(self.generate_sync, prompt)
