
from uuid import uuid4

from app.services.vector_service import store_document_chunks


document_id = str(uuid4())

chunks = [
    "Python is a high-level programming language.",
    "Django is a Python framework used for web development.",
    "FastAPI is used to build APIs."
]

metadata = {
    "document_id": document_id,
    "filename": "python_notes.txt"
}

stored_ids = store_document_chunks(chunks, metadata)

print("Chunks stored successfully!")
print("Document ID:", document_id)
print("Stored chunk IDs:", stored_ids)
print("Total chunks stored:", len(stored_ids))
