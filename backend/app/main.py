
from fastapi import FastAPI

from app.routes.documents import router as document_router
from app.routes.questions import router as question_router


app = FastAPI(
    title="Simple RAG System",
    description="A beginner-friendly Retrieval Augmented Generation application",
    version="1.0.0"
)

app.include_router(document_router)
app.include_router(question_router)


@app.get("/")
def home():
    return {"message": "Welcome to Simple RAG System"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Simple RAG API is running"
    }
