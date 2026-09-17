from unittest.mock import MagicMock, patch

from langchain_core.documents import Document

from rag.rag_chain import ask_documents


@patch("rag.rag_chain.get_llm")
@patch("rag.rag_chain.load_vector_store")
def test_retrieval_uses_only_current_question(
    mock_load_vector_store,
    mock_get_llm,
):
    vector_store = MagicMock()

    vector_store.similarity_search.return_value = [
        Document(
            page_content=(
                "Employees may carry forward "
                "up to 5 annual leave days."
            ),
            metadata={
                "source": "employee_handbook.txt"
            },
        )
    ]

    mock_load_vector_store.return_value = vector_store

    llm = MagicMock()

    llm.invoke.return_value = MagicMock(
        content="Employees may carry forward up to 5 days."
    )

    mock_get_llm.return_value = llm

    current_question = (
        "How many of those can I carry forward?"
    )

    history = (
        "User: How many annual leave days "
        "do employees receive?\n"
        "Assistant: Employees receive 24 days."
    )

    answer, documents = ask_documents(
        question=current_question,
        history=history,
    )

    vector_store.similarity_search.assert_called_once_with(
        current_question,
        k=3,
    )

    assert "5 days" in answer

    assert (
        documents[0].metadata["source"]
        == "employee_handbook.txt"
    )
