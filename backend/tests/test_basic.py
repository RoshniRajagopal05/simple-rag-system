
from app.services.chunk_service import split_document


def test_split_document_returns_chunks():
    text = "Python is a programming language."

    chunks = split_document(text)

    assert len(chunks) == 1
    assert chunks[0] == text


def test_split_document_empty_text():
    text = ""

    chunks = split_document(text)

    assert chunks == []
