
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Chunk configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def split_document(text: str):
    """
    Divide extracted document text into smaller chunks.
    """

    if not text or not text.strip():
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = text_splitter.split_text(text)

    return chunks
