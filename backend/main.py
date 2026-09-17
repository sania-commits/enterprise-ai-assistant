from fastapi import FastAPI

from agents.graph import agent_graph
from backend.schemas import AskRequest, AskResponse


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
    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    result = agent_graph.invoke(
        {
            "question": request.question,
            "route": "",
            "answer": "",
            "sources": [],
            "history": [],
        },
        config=config,
    )

    return AskResponse(
        answer=result["answer"],
        route=result["route"],
        sources=result["sources"],
    )