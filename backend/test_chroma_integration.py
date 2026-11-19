
from pathlib import Path

from app.config import GEMINI_API_KEY
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


# 1. Configure Gemini embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GEMINI_API_KEY,
    task_type="RETRIEVAL_DOCUMENT"
)


# 2. Configure ChromaDB storage location
CHROMA_DIR = Path(__file__).resolve().parent / "chroma_db"


# 3. Sample document chunks
texts = [
    "Python is a high-level programming language.",
    "Python supports object-oriented programming.",
    "Django is a Python framework used for web development.",
    "FastAPI is used to build APIs using Python."
]


# 4. Create a ChromaDB collection and store the texts
vector_store = Chroma.from_texts(
    texts=texts,
    embedding=embeddings,
    collection_name="documents",
    persist_directory=str(CHROMA_DIR),
    ids=["chunk_1", "chunk_2", "chunk_3", "chunk_4"]
)


print("Documents stored successfully in ChromaDB!")

# 5. Search for similar document chunks
query = "Which Python framework can be used to build websites?"

results = vector_store.similarity_search(query, k=2)


print("\nRelevant document chunks:")

for result in results:
    print("-", result.page_content)


# Remove the four manually inserted test records
vector_store.delete(
    ids=["chunk_1", "chunk_2", "chunk_3", "chunk_4"]
)

print("Sample test records deleted successfully!")