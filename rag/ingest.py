from pathlib import Path
import shutil

from rag.document_loader import load_document
from rag.text_splitter import split_documents
from rag.vector_store import (
    PERSIST_DIRECTORY,
    create_vector_store,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIRECTORY = PROJECT_ROOT / "data" / "raw"


def ingest_documents():
    """Build the vector database from enterprise documents."""

    supported_files = sorted(
        [
            path
            for path in DATA_DIRECTORY.iterdir()
            if path.suffix.lower() in {".txt", ".pdf"}
        ]
    )

    if not supported_files:
        raise FileNotFoundError(
            "No supported documents found in data/raw."
        )

    documents = []

    for file_path in supported_files:
        print(f"Loading: {file_path}")

        loaded_documents = load_document(
            str(file_path)
        )

        documents.extend(loaded_documents)

    chunks = split_documents(documents)

    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks created: {len(chunks)}")

    vector_database = Path(PERSIST_DIRECTORY)

    if vector_database.exists():
        for item in vector_database.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

        print(
            f"Cleared existing vector database: "
            f"{PERSIST_DIRECTORY}"
        )

    create_vector_store(chunks)


if __name__ == "__main__":
    ingest_documents()
