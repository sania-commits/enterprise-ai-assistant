from langchain_google_genai import ChatGoogleGenerativeAI

from backend.config import settings


def get_llm():
    """Create and return the Gemini LLM."""

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=settings.google_api_key,
    )

    return llm
