from rag.vector_store import load_vector_store


def retrieve_sources(question: str, k: int = 3):
    """Return source filenames retrieved for a question."""

    vector_store = load_vector_store()

    documents = vector_store.similarity_search(
        question,
        k=k,
    )

    return [
        document.metadata.get("source", "")
        for document in documents
    ]


def test_remote_work_retrieval():
    sources = retrieve_sources(
        "How many days can employees work remotely?"
    )

    assert any(
        "remote_work_policy.txt" in source
        for source in sources
    )


def test_security_policy_retrieval():
    sources = retrieve_sources(
        "What should I do if I receive a phishing attempt?"
    )

    assert any(
        "security_policy.txt" in source
        for source in sources
    )


def test_leave_policy_retrieval():
    sources = retrieve_sources(
        "How many annual leave days do employees receive?"
    )

    assert any(
        "employee_handbook.txt" in source
        for source in sources
    )
