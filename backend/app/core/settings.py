from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    INTENT_SERVICE_HOST: str = "intent-service"
    INTENT_SERVICE_PORT: int = 50051
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "gemma3:4b"
    OLLAMA_API_TYPE: str = "chat"
    API_PORT: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()

