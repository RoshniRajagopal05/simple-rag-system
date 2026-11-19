
from unittest.mock import patch

from langchain_core.documents import Document

from app.services.retrieval_service import retrieve_relevant_chunks


@patch("app.services.retrieval_service.vector_store.similarity_search_with_relevance_scores")
def test_retrieve_relevant_chunks(mock_search):

    mock_search.return_value = [
        (
            Document(
                page_content="Django is a Python web framework.",
                metadata={"filename": "python.txt", "chunk_index": 0}
            ),
            0.85
        ),
        (
            Document(
                page_content="France is in Europe.",
                metadata={"filename": "general.txt", "chunk_index": 1}
            ),
            0.60
        )
    ]

    results = retrieve_relevant_chunks(
        question="Which Python framework is used for web development?",
        k=3
    )

    assert len(results) == 1
    assert results[0]["content"] == "Django is a Python web framework."
    assert results[0]["metadata"]["filename"] == "python.txt"


@patch("app.services.retrieval_service.vector_store.similarity_search_with_relevance_scores")
def test_reject_irrelevant_chunks(mock_search):

    mock_search.return_value = [
        (
            Document(
                page_content="France is in Europe.",
                metadata={"filename": "general.txt"}
            ),
            0.60
        )
    ]

    results = retrieve_relevant_chunks(
        question="What is the capital of France?"
    )

    assert results == []


@patch("app.services.retrieval_service.vector_store.similarity_search_with_relevance_scores")
def test_empty_question(mock_search):

    results = retrieve_relevant_chunks(question="")

    assert results == []
    mock_search.assert_not_called()


@patch("app.services.retrieval_service.vector_store.similarity_search_with_relevance_scores")
def test_document_specific_filter(mock_search):

    mock_search.return_value = []

    document_id = "test-document-123"

    retrieve_relevant_chunks(
        question="Explain Python",
        k=3,
        document_id=document_id
    )

    mock_search.assert_called_once_with(
        query="Explain Python",
        k=3,
        filter={"document_id": document_id}
    )
