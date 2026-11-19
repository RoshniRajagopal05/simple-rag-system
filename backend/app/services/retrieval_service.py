
from app.services.vector_service import vector_store

RELEVANCE_THRESHOLD = 0.70


def retrieve_relevant_chunks(
    question: str,
    k: int = 3,
    document_id: str | None = None
):
    if not question or not question.strip():
        return []

    search_filter = None

    if document_id:
        search_filter = {"document_id": document_id}

    results = vector_store.similarity_search_with_relevance_scores(
        query=question,
        k=k,
        filter=search_filter
    )

    retrieved_chunks = []

    for document, score in results:

        # Reject chunks below the relevance threshold
        if score < RELEVANCE_THRESHOLD:
            continue

        retrieved_chunks.append({
            "content": document.page_content,
            "metadata": document.metadata
        })

    return retrieved_chunks
