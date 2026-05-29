# Banking AI Agent Backend

This is the API Gateway for the Banking AI Agent System.

## Architecture Overview
The system uses a microservice architecture:
1. **Backend / API Gateway**: FastAPI app that accepts user queries, orchestrates a workflow (Intent -> Priority -> Policy -> Route -> Validate -> Draft), and talks to the intent microservice via gRPC.
2. **Intent Service**: A gRPC service connecting to Ollama to classify banking intents.
3. **Frontend**: Streamlit app for interactions.
4. **Ollama**: Local instance generating LLM responses.

## Generating gRPC Code
```bash
cd ../intent_service
make generate
```

## Running with Docker Compose
From the root folder:
```bash
docker-compose up --build
```
(Make sure to pull `gemma3:4b` using `ollama pull gemma3:4b` on your host first)

## Test API
```bash
curl -X POST http://localhost:8000/run-agent \
  -H "Content-Type: application/json" \
  -d '{"message": "I want to dispute a transaction"}'
```
