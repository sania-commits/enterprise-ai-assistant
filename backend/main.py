from fastapi import FastAPI

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
