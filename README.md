# Enterprise AI Assistant

An end-to-end enterprise Generative AI application combining Retrieval-Augmented Generation (RAG), AI agent routing, conversational memory, tool use, REST APIs, evaluation, and containerized deployment.

The system intelligently routes user queries between enterprise document retrieval, mathematical calculation, and general-purpose LLM reasoning.

## Key Features

- Retrieval-Augmented Generation (RAG) over enterprise documents
- LangGraph-based multi-route AI agent workflow
- Google Gemini LLM integration
- Gemini embeddings for semantic document retrieval
- ChromaDB persistent vector database
- Conversation memory using LangGraph checkpointing
- Safe AST-based calculator tool
- FastAPI REST backend
- Streamlit conversational frontend
- Source attribution for document-based answers
- RAG and routing evaluation framework
- Automated pytest test suite
- Dockerized backend, frontend, and ingestion services
- Docker Compose orchestration
- Backend health checks and service dependencies
- Environment-based secret management
- Service-specific Docker dependency optimization

## System Architecture

```text
                    ┌─────────────────────┐
                    │        User         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Streamlit Frontend  │
                    │      :8501          │
                    └──────────┬──────────┘
                               │ HTTP / JSON
                               ▼
                    ┌─────────────────────┐
                    │  FastAPI Backend    │
                    │       :8000         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  LangGraph Router   │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ┌──────────┐    ┌────────────┐    ┌──────────┐
        │   RAG    │    │ Calculator │    │ General  │
        │  Agent   │    │    Tool    │    │   LLM    │
        └────┬─────┘    └────────────┘    └──────────┘
             │
             ▼
        ┌──────────┐
        │ ChromaDB │
        └────┬─────┘
             │
             ▼
      Enterprise Documents

## Agent Routing

The LangGraph workflow classifies each incoming request into one of three routes:

| Route | Purpose |
|---|---|
| `rag` | Enterprise policies, internal procedures, security rules, remote-work policies, and other document-based questions |
| `calculator` | Arithmetic and mathematical calculations |
| `general` | General knowledge, technical, educational, and conceptual questions |

Conversation history is maintained through LangGraph checkpointing and supplied to relevant agent nodes to support conversational follow-up questions.

## RAG Pipeline

The Retrieval-Augmented Generation pipeline processes enterprise documents through the following workflow:

```text
Enterprise Documents
        ↓
Document Loader
        ↓
Recursive Text Splitting
        ↓
Gemini Embeddings
        ↓
ChromaDB
        ↓
Similarity Search
        ↓
Relevant Document Context
        ↓
Gemini LLM
        ↓
Grounded Answer + Sources
```

For enterprise-document questions, the assistant is instructed to answer using the retrieved document context. If sufficient information is not available in the supplied documents, the RAG prompt instructs the model to return an insufficient-information response.

Conversation history can help interpret references in the current question, but it is not treated as factual evidence in place of retrieved documents.

## Technology Stack

| Layer | Technology |
|---|---|
| LLM | Google Gemini |
| Embeddings | Gemini Embeddings |
| Agent Orchestration | LangGraph |
| LLM Framework | LangChain |
| Vector Database | ChromaDB |
| Backend API | FastAPI |
| Frontend | Streamlit |
| Validation / Settings | Pydantic Settings |
| Testing | Pytest |
| Containers | Docker |
| Orchestration | Docker Compose |
| Language | Python 3.12 |

## Project Structure

```text
enterprise-ai-assistant/
├── agents/                     # LangGraph state, routing, nodes and tools
├── backend/                    # FastAPI application and Gemini configuration
├── data/
│   ├── raw/                    # Source enterprise documents
│   └── processed/
├── evaluation/                 # RAG and groundedness evaluation
├── frontend/                   # Streamlit chat interface
├── rag/                        # Loading, chunking, embeddings and retrieval
├── tests/                      # Automated tests
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
├── requirements.txt            # Local development dependencies
├── requirements-backend.txt    # Backend container dependencies
├── requirements-frontend.txt   # Frontend container dependencies
├── .env.example
└── README.md
```

## Local Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd enterprise-ai-assistant
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv-4
source .venv-4/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create the local environment file:

```bash
cp .env.example .env
```

Then provide your own Gemini API key in `.env`:

```env
GOOGLE_API_KEY=your-google-api-key-here
```

Never commit the real `.env` file or API keys.

## Document Ingestion

Place supported enterprise `.txt` or `.pdf` documents inside:

```text
data/raw/
```

Build the ChromaDB vector database with:

```bash
python -m rag.ingest
```

The ingestion pipeline loads the documents, splits them into chunks, creates Gemini embeddings, and stores the resulting vectors in the persistent ChromaDB collection.

## Run Locally

Start the FastAPI backend:

```bash
uvicorn backend.main:app --reload
```

The API is available at:

```text
http://127.0.0.1:8000
```

In another terminal, start the Streamlit frontend:

```bash
streamlit run frontend/app.py
```

The application is available at:

```text
http://127.0.0.1:8501
```
## Docker Deployment

The application is containerized as separate backend, frontend, and document-ingestion services.

### Build the application

```bash
docker compose build backend frontend
```

### Build the vector database

The ingestion service uses a persistent Docker volume for ChromaDB:

```bash
docker compose --profile tools run --rm ingest
```

Run ingestion before starting the application when initializing a new vector database.

### Start the application

```bash
docker compose up -d
```

Check container status:

```bash
docker compose ps
```

The backend includes a health check at:

```text
http://127.0.0.1:8000/health
```

The Streamlit interface is available at:

```text
http://127.0.0.1:8501
```

### Stop the application

```bash
docker compose down
```

The ChromaDB data is stored in the `chroma_data` Docker volume so vector data can persist across normal container recreation.

## API

### Health Check

```http
GET /health
```

### Ask the Assistant

```http
POST /ask
Content-Type: application/json
```

Example request:

```json
{
  "question": "How many annual leave days do full-time employees receive?",
  "thread_id": "example-session"
}
```

Example response structure:

```json
{
  "answer": "Full-time employees receive 24 paid annual leave days per calendar year.",
  "route": "rag",
  "sources": [
    "employee_handbook.txt"
  ]
}
```

`thread_id` allows LangGraph to associate conversation state with a conversation while the application is running.

## Testing

The project contains automated tests covering:

- FastAPI endpoints and error handling
- LangGraph conversation memory
- Agent routing
- Safe calculator execution
- RAG-chain behavior using mocks
- Retrieval integration
- Evaluation logic

Run the offline regression suite without intentionally invoking the live Gemini generation API:

```bash
pytest \
  tests/test_api.py \
  tests/test_memory.py \
  tests/test_tools.py \
  tests/test_router.py \
  tests/test_rag_chain.py \
  tests/test_evaluation.py \
  -q
```

Verified result during development:

```text
26 passed
```

Retrieval integration tests are maintained separately because they can require the configured embedding service:

```bash
pytest tests/test_retrieval.py -q
```

## Evaluation

The repository includes evaluation components for:

- expected agent routing
- document retrieval
- expected answer keywords
- insufficient-context/refusal behavior
- deterministic groundedness checks

Evaluation cases are stored separately from application logic so the assistant can be tested against repeatable scenarios.

## Engineering & Security Decisions

### Safe Calculator

Mathematical expressions are evaluated through a restricted Python AST rather than `eval()`.

The calculator restricts supported operators and applies limits to expression length, exponent size, and result magnitude.

### RAG Grounding

For enterprise-document questions, retrieved document content is treated as the factual evidence for the answer. Conversation history is used to understand conversational references rather than as a replacement for retrieved evidence.

### Secret Management

The Gemini API key is supplied through environment variables. The real `.env` file is excluded from both Git and the Docker build context.

### API Resilience

The backend converts provider quota failures into a controlled HTTP `429` response and other service failures into a controlled service-unavailable response rather than exposing raw application errors to the frontend.

### Container Health

Docker Compose waits for the backend health check before starting the frontend, reducing startup-order failures.

### Docker Optimization

Backend and frontend services use separate dependency files so each image contains only the packages required by that service.

During development, this reduced the reported Docker image sizes from approximately:

| Service | Before | Optimized |
|---|---:|---:|
| Backend | 1.42 GB | 955 MB |
| Frontend | 1.42 GB | 779 MB |
| Ingestion | 1.42 GB | 955 MB |

These measurements are development-build observations and can vary with dependency versions, Docker versions, platform, and build cache.

## Current Limitations

- Conversation checkpoints currently use in-memory storage and do not survive application restarts.
- Gemini API availability and quotas depend on the configured Google account/project.
- The included enterprise documents are demonstration data rather than a production corporate knowledge base.
- Authentication and user-level authorization are not yet implemented.
- Production deployments should use persistent managed storage and an appropriate secrets-management solution.

## Future Improvements

- Persistent conversation checkpoint storage
- Authentication and role-based access control
- Additional enterprise tools and agent routes
- Improved retrieval relevance filtering and reranking
- Larger automated RAG evaluation dataset
- Observability, structured logging, and tracing
- CI/CD pipeline
- Cloud deployment
