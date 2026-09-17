from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from agents.graph import agent_graph
from backend.schemas import AskRequest, AskResponse


app = FastAPI(
    title="Enterprise AI Assistant API",
    description="Backend API for an enterprise RAG and AI agent platform",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

    try:
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

    except Exception as error:
        error_text = str(error).lower()

        if (
            "429" in error_text
            or "resource_exhausted" in error_text
            or "quota" in error_text
        ):
            raise HTTPException(
                status_code=429,
                detail=(
                    "AI provider quota temporarily exceeded. "
                    "Please try again later."
                ),
            ) from error

        raise HTTPException(
            status_code=503,
            detail=(
                "The AI service is temporarily unavailable. "
                "Please try again later."
            ),
        ) from error

    return AskResponse(
        answer=result["answer"],
        route=result["route"],
        sources=result["sources"],
    )