from fastapi import FastAPI
from backend.schemas import AskRequest, AskResponse
from agents.graph import agent_graph

app = FastAPI(
    title="Enterprise AI Assistant API",
    description="Backend API for an enterprise RAG and AI agent platform",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Enterprise AI Assistant API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    result = agent_graph.invoke(
        {
            "question": request.question,
            "route": "",
            "answer": "",
            "sources": [],
        }
    )

    return AskResponse(
        answer=result["answer"],
        route=result["route"],
        sources=result["sources"],
    )
