
from app.services.retrieval_service import retrieve_relevant_chunks

DOCUMENT_ID = "2297b127-f630-491c-86fa-ecb5782580b2"

questions = [
    "Which Python framework can be used for web development?",
    "What is the capital of France?"
]

for question in questions:

    print("\nQuestion:", question)

    results = retrieve_relevant_chunks(
        question=question,
        k=3,
        document_id=DOCUMENT_ID
    )

    if not results:
        print("No relevant chunks found.")

    else:
        print("\nRetrieved chunks:")

        for index, result in enumerate(results, start=1):
            print(f"\nResult {index}")
            print("Content:", result["content"])
            print("Metadata:", result["metadata"])
