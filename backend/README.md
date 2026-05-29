# Banking AI Agent Backend

The **Banking AI Agent Backend** serves as the API Gateway and Workflow Orchestrator for the Banking AI Agent System. It is built with FastAPI and is responsible for managing the sequential execution of agentic nodes to process customer inquiries.

## Core Responsibilities

*   **API Gateway**: Provides RESTful endpoints for the frontend and external clients.
*   **Workflow Orchestration**: Manages the state and transition between different processing nodes (Intent, Priority, Policy, etc.).
*   **gRPC Client**: Interfaces with the `intent_service` to perform sub-tasks like intent classification.
*   **Validation & Response Generation**: Ensures all necessary information is collected and generates professional draft replies.

## Architecture & Workflow

The backend uses a modular node-based architecture. When a request is received at `/run-agent`, the `orchestrator` executes the following sequence:

1.  **Intent Node**: Communicates via gRPC with the `intent_service` to classify the user's message.
2.  **Priority Node**: Assigns an urgency level (LOW, MEDIUM, HIGH) to the request.
3.  **Policy Node**: Checks the request against banking logic and compliance rules.
4.  **Router Node**: Determines the internal path for further processing.
5.  **Validation Node**: Identifies any missing information required from the user.
6.  **Draft Node**: Synthesizes the final response and next steps.

## Tech Stack

*   **FastAPI**: Web framework for the REST API.
*   **Pydantic Settings**: Configuration management via environment variables.
*   **gRPC**: Client implementation for microservice communication.
*   **Uvicorn**: ASGI server for production deployment.

## Getting Started

### Prerequisites

*   Python 3.11+
*   Working `intent_service` (for gRPC calls)
*   Ollama (if testing end-to-end)

### Installation

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  (Optional) Generate gRPC stubs if the proto file has changed:
    ```bash
    # Follow instructions in intent_service/README.md and copy stubs to app/clients/intent_grpc/
    ```

### Configuration

The backend is configured via environment variables or a `.env` file:

| Variable | Default | Description |
| :--- | :--- | :--- |
| `INTENT_SERVICE_HOST` | `intent-service` | Hostname of the gRPC intent service |
| `INTENT_SERVICE_PORT` | `50051` | Port of the gRPC intent service |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | URL for the Ollama LLM backend |
| `OLLAMA_MODEL` | `gemma3:4b` | Target LLM model |
| `API_PORT` | `8000` | Port for the FastAPI server |

### Running Locally

```bash
python run.py
```

## API Documentation

Once the server is running, you can access the interactive documentation at:
*   **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
*   **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Key Endpoints

#### `POST /run-agent`
Executes the full agentic workflow for a given message.

**Request Body**:
```json
{
  "message": "string",
  "customer_id": "string (optional)"
}
```

#### `GET /health`
Returns the status of the backend service.

#### `GET /config`
Returns the current active configuration (host, port, model).

## Project Structure

```text
backend/
├── app/
│   ├── agent/         # Orchestrator and workflow logic
│   ├── clients/       # gRPC and external API clients
│   ├── core/          # Settings, schemas, and shared utilities
│   ├── nodes/         # Individual agentic processing units
│   └── main.py        # FastAPI application entry point
├── Dockerfile         # Containerization setup
├── requirements.txt   # Python dependencies
└── run.py             # Server startup script
```
