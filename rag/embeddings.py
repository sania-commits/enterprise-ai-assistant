from langchain_google_genai import GoogleGenerativeAIEmbeddings

from backend.config import settings


def get_embeddings():
    """Create and return the Gemini embedding model."""

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=settings.google_api_key,
    )

    return embeddings
