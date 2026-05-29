from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "gemma3:4b"
    # "chat" dùng /api/chat (OpenAI-compatible, Colab/Pinggy)
    # "generate" dùng /api/generate (Ollama native localhost)
    OLLAMA_API_TYPE: str = "chat"
    GRPC_PORT: int = 50051

    class Config:
        env_file = ".env"

settings = Settings()

