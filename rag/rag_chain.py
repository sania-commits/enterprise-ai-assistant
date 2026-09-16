from backend.llm import get_llm
from rag.vector_store import load_vector_store

def extract_text(content):
    """Extract plain text from an LLM response."""

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        return "".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )

    return str(content)

def ask_documents(question: str, k: int = 3):
    """Answer a question using retrieved document context."""

    vector_store = load_vector_store()

    documents = vector_store.similarity_search(
        question,
        k=k,
    )

    context = "\n\n".join(
        document.page_content for document in documents
    )

    prompt = f"""
You are an enterprise AI assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I don't have enough information in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""

    llm = get_llm()
    response = llm.invoke(prompt)

    return extract_text(response.content), documents
