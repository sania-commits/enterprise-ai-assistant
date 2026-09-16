from backend.llm import get_llm
from agents.state import AgentState


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


def router_node(state: AgentState):
    """Decide whether the question needs RAG or general LLM knowledge."""

    question = state["question"]

    prompt = f"""
You are a routing component for an enterprise AI assistant.

Classify the user's question into exactly one category:

rag
- Questions about company policies, employees, internal procedures,
  security rules, remote work, leave, or company-specific information.

general
- General knowledge, educational, technical, or conceptual questions
  that do not require company documents.

Return ONLY one word:
rag
or
general

Question:
{question}
"""

    llm = get_llm()
    response = llm.invoke(prompt)

    route = extract_text(response.content).strip().lower()

    if route not in {"rag", "general"}:
        route = "general"

    return {
        "route": route
    }
