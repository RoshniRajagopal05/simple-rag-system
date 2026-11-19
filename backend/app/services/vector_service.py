
from pathlib import Path

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config import GEMINI_API_KEY


# ChromaDB storage directory
CHROMA_DIR = Path(__file__).resolve().parents[2] / "chroma_db"

# Collection name
COLLECTION_NAME = "documents"


# Initialize Gemini embedding model
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GEMINI_API_KEY,
    task_type="RETRIEVAL_DOCUMENT"
)


# Initialize ChromaDB
vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=str(CHROMA_DIR)
)


def store_document_chunks(chunks: list[str], metadata: dict):
    """
    Store document chunks and their embeddings in ChromaDB.
    """

    if not chunks:
        return []

    ids = [
        f"{metadata['document_id']}_chunk_{index}"
        for index in range(len(chunks))
    ]

    metadatas = [
        {
            **metadata,
            "chunk_index": index
        }
        for index in range(len(chunks))
    ]

    vector_store.add_texts(
        texts=chunks,
        metadatas=metadatas,
        ids=ids
    )

    return ids
