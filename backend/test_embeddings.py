
from app.config import GEMINI_API_KEY
from langchain_google_genai import GoogleGenerativeAIEmbeddings


# Check whether the API key is available
if not GEMINI_API_KEY:
    raise ValueError("Gemini API key not found. Check your .env file.")


# Initialize the Gemini embedding model
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GEMINI_API_KEY,
    task_type="RETRIEVAL_DOCUMENT"
)


# Sample document text
text = "Python is a high-level programming language."


# Generate the embedding
vector = embeddings.embed_documents([text])[0]


# Display the result
print("Embedding generated successfully!")
print("Vector dimensions:", len(vector))
print("First five values:", vector[:5])
