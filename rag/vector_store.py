from langchain_chroma import Chroma

from rag.embeddings import get_embeddings


from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PERSIST_DIRECTORY = PROJECT_ROOT / "chroma_db"


def create_vector_store(chunks):
    """Create a persistent Chroma vector store from document chunks."""

    embeddings = get_embeddings()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY,
        collection_name="enterprise_documents",
    )

    return vector_store


def load_vector_store():
    """Load the existing persistent Chroma vector store."""

    embeddings = get_embeddings()

    vector_store = Chroma(
        collection_name="enterprise_documents",
        embedding_function=embeddings,
        persist_directory=PERSIST_DIRECTORY,
    )

    return vector_store
