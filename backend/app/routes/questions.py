
import logging

from fastapi import APIRouter, HTTPException

from app.schemas.question import QuestionRequest
from app.services.retrieval_service import retrieve_relevant_chunks
from app.services.generation_service import generate_answer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/ask/")
def ask_question(request: QuestionRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    results = retrieve_relevant_chunks(
        question=request.question,
        k=3,
        document_id=request.document_id
    )

    try:
        answer = generate_answer(
            question=request.question,
            retrieved_chunks=results
        )

    except RuntimeError as error:
        logger.error("Question answering failed: %s", error)

        raise HTTPException(
            status_code=503,
            detail="The AI service is temporarily unavailable. Please try again later."
        ) from error

    sources = []

    for result in results:
        sources.append({
            "filename": result["metadata"].get("filename"),
            "document_id": result["metadata"].get("document_id"),
            "chunk_index": result["metadata"].get("chunk_index"),
            "content": result["content"]
        })

    return {
        "question": request.question,
        "answer": answer,
        "total_sources": len(sources),
        "sources": sources
    }
