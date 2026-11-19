
from app.services.vector_service import vector_store

DOCUMENT_ID = "2297b127-f630-491c-86fa-ecb5782580b2"

questions = [
    "Which Python framework can be used for web development?",
    "What is the capital of France?"
]

for question in questions:
    print("\nQuestion:", question)

    results = vector_store.similarity_search_with_relevance_scores(
        query=question,
        k=3,
        filter={"document_id": DOCUMENT_ID}
    )

    if not results:
        print("No matching results found.")
        continue

    for document, score in results:
        print("\nRelevance score:", round(score, 4))
        print("Content:", document.page_content)
