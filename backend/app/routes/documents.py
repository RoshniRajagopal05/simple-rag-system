
import logging
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.document_service import (
    extract_document,
    save_document
)
from app.services.chunk_service import split_document
from app.services.vector_service import store_document_chunks


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload/")
async def upload_document(file: UploadFile = File(...)):

    try:
        # 1. Read uploaded file
        file_content = await file.read()

        # 2. Extract text
        extracted_text = extract_document(
            file_content,
            file.filename or ""
        )

        # 3. Split extracted text into chunks
        chunks = split_document(extracted_text)

        # 4. Generate a unique document ID
        document_id = str(uuid4())

        # 5. Save original document
        saved_filename = save_document(
            file_content,
            file.filename or ""
        )

        # 6. Prepare document metadata
        metadata = {
            "document_id": document_id,
            "filename": file.filename or "unknown"
        }

        # 7. Store chunks and embeddings in ChromaDB
        stored_chunk_ids = store_document_chunks(
            chunks,
            metadata
        )

        # 8. Return upload response
        return {
            "message": "Document uploaded and stored successfully",
            "document_id": document_id,
            "original_filename": file.filename,
            "content_type": file.content_type,
            "character_count": len(extracted_text),
            "total_chunks": len(chunks),
            "stored_chunks": len(stored_chunk_ids)
        }

    except HTTPException:
        raise

    except Exception as error:
        logger.exception("Document upload failed")

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while uploading the document."
        ) from error

    finally:
        await file.close()
