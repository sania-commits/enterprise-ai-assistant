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
            if (
                isinstance(block, dict)
                and block.get("type") == "text"
            )
        )

    return str(content)


def ask_documents(
    question: str,
    history: str = "",
    k: int = 3,
):
    """Answer using retrieved enterprise documents."""

    vector_store = load_vector_store()

    # Retrieve documents using only the current question.
    documents = vector_store.similarity_search(
        question,
        k=k,
    )

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = f"""
You are an enterprise AI assistant.

Answer the user's current question using ONLY the
provided document context.

Conversation history may be used only to understand
references in the current question.

Do not use conversation history as factual evidence.

If the answer cannot be found in the document context,
say exactly:

"I don't have enough information in the provided documents."

Conversation history:
{history}

Document context:
{context}

Current question:
{question}

Answer:
"""

    llm = get_llm()

    response = llm.invoke(prompt)

    return (
        extract_text(response.content),
        documents,
    )