from agents.state import AgentState
from backend.llm import get_llm
from rag.rag_chain import ask_documents


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


def rag_node(state: AgentState):
    """Answer using enterprise documents."""

    answer, documents = ask_documents(state["question"])

    sources = sorted(
        {
            document.metadata.get("source", "unknown")
            for document in documents
        }
    )

    return {
        "answer": answer,
        "sources": sources,
    }


def general_node(state: AgentState):
    """Answer general questions using the LLM."""

    llm = get_llm()

    response = llm.invoke(state["question"])

    answer = extract_text(response.content)

    return {
        "answer": answer,
        "sources": [],
    }
