# Banking AI Agent System

This project implements a multi-service AI agent system designed for banking customer service. The architecture leverages distributed microservices to process user inquiries, assess priorities, and generate automated draft replies using Large Language Models (LLMs).

## Architecture Overview

The system follows a microservice design pattern, coordinating multiple components to handle complex banking workflows.

```text
       [ User Browser ]
               ↓
      [ Frontend ] (Streamlit)
               ↓ 
               ↓ REST API
               ↓
      [ Backend ] (FastAPI / API Gateway / Orchestrator)
               ↓
               ↓ gRPC
               ↓
      [ Intent Service ] (Python / gRPC)
               ↓
               ↓ HTTP
               ↓
      [ Ollama ] (LLM Backend)
```

### Communication Flow

1.  **Frontend → Backend**: RESTful communication for submitting user messages and retrieving processing results.
2.  **Backend → Intent Service**: High-performance gRPC calls to classify user intent and obtain reasoning.
3.  **Intent Service → Ollama**: HTTP requests to the LLM API for natural language understanding and text generation.

## Prerequisites

Ensure the following software is installed on your system:

*   **Python 3.10+**: Required for local development.
*   **Docker & Docker Compose**: Necessary for containerized deployment.
*   **Ollama**: Required for running the LLM backend locally.
*   **Make**: Recommended for managing gRPC code generation.

## Project Structure

```text
banking-service/
├── backend/                # FastAPI application, orchestrator, and gRPC client
├── frontend/               # Streamlit web interface
├── intent_service/         # gRPC service for intent classification
├── docker-compose.yml      # Orchestration configuration for all services
└── README.md               # Project documentation
```

## Local Development Setup

To run the services manually for development, follow these steps:

### 1. LLM Backend (Ollama)
Install Ollama and pull the required model:
```bash
ollama serve
# In a new terminal:
ollama pull gpt-oss:20b
```

### 2. Intent Service
Install dependencies and start the gRPC server:
```bash
cd intent_service
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
pip install -r requirements.txt
python server.py
```
*   **Port**: 50051 (gRPC)

### 3. Backend
Install dependencies and start the API Gateway:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
pip install -r requirements.txt
python run.py
```
*   **Port**: 8000 (REST)
*   **Endpoints**: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)

### 4. Frontend
Install dependencies and start the web interface:
```bash
cd frontend
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
pip install -r requirements.txt
streamlit run interface.py
```
*   **Port**: 8501
*   **URL**: [http://localhost:8501](http://localhost:8501)

## gRPC Code Generation

The communication between the Backend and Intent Service is defined in `intent_service/intent_service.proto`.

### Commands
From the `intent_service` directory:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. intent_service.proto
```

### Synchronization
After generation, copy the `*_pb2.py` and `*_pb2_grpc.py` files to:
`backend/app/clients/intent_grpc/`

## Docker Deployment

### Building Individual Images
```bash
docker build -t banking-backend ./backend
docker build -t intent-service ./intent_service
docker build -t banking-frontend ./frontend
```

### Running with Docker Compose
From the root directory:
```bash
# Build and start all containers
docker-compose up --build

# Stop the system
docker-compose down
```

## Service Responsibility Matrix

| Service | Container Name | Role |
| :--- | :--- | :--- |
| **Backend** | `banking-backend` | API Gateway, Workflow Orchestrator, Node Execution |
| **Intent Service** | `intent-service` | gRPC Server, NLP Task Execution, LLM Interface |
| **Frontend** | `banking-frontend` | User Presentation, Result Visualization |

## API Usage Examples

### Health Check
**Request**: `GET /health`
**Response**:
```json
{
  "status": "ok",
  "service": "banking-agent"
}
```

### Configuration
**Request**: `GET /config`
**Response**:
```json
{
  "intent_host": "intent-service",
  "intent_port": 50051,
  "ollama_host": "http://localhost:11434",
  "ollama_model": "gpt-oss:20b"
}
```

### Run Agent
**Request**: `POST /run-agent`
```json
{
  "message": "I lost my credit card today.",
  "customer_id": "user123"
}
```

**Response**:
```json
{
  "intent": "card_loss",
  "confidence": 0.95,
  "priority": "HIGH",
  "policy": "Blocked card procedure must be followed.",
  "draft_reply": "We are sorry to hear that. Your card has been provisionally blocked...",
  "missing_info": [],
  "next_action": "card_replacement_workflow",
  "processing_time": 1.42
}
```

## Troubleshooting

### gRPC Connection Failures
*   Check if `intent-service` is healthy using `docker ps`.
*   Verify `INTENT_SERVICE_HOST` and `INTENT_SERVICE_PORT` environment variables in `docker-compose.yml`.
*   Ensure generated protobuf files are present in the backend.

### Ollama Issues
*   Verify Ollama is running (`curl http://localhost:11434/api/tags`).
*   Ensure the model `gpt-oss:20b` has been pulled.
*   Check the `OLLAMA_BASE_URL` if Ollama is running on a different machine/port.

### Missing Protobuf Files
If the backend crashes with import errors like `ModuleNotFoundError: No module named 'app.clients.intent_grpc'`, run the gRPC generation steps and ensure files are copied to the backend directory.
