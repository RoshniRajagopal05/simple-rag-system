
from io import BytesIO
from pathlib import Path
from uuid import uuid4
import logging

from pypdf import PdfReader
from fastapi import HTTPException


logger = logging.getLogger(__name__)

UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def extract_document(file_content: bytes, filename: str):
    """
    Extract text from PDF or TXT documents.
    """

    extension = Path(filename).suffix.lower()

    # 1. Validate file extension
    if extension not in [".pdf", ".txt"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported."
        )

    # 2. Validate empty file
    if not file_content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # 3. Validate file size
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the 10 MB limit."
        )

    # 4. Extract PDF content
    if extension == ".pdf":

        try:
            reader = PdfReader(BytesIO(file_content), strict=False)

            # Check PDF encryption
            if reader.is_encrypted:
                raise HTTPException(
                    status_code=400,
                    detail="Password-protected PDFs are not supported."
                )

            extracted_text = []

            # Extract text page by page
            for page_number, page in enumerate(reader.pages, start=1):

                page_text = page.extract_text() or ""

                if page_text.strip():
                    extracted_text.append(
                        f"Page {page_number}:\n{page_text}"
                    )

            text = "\n\n".join(extracted_text)

        except HTTPException:
            raise

        except Exception as error:

            print("========== PDF DEBUG ==========")
            print("Filename:", filename)
            print("Error type:", type(error).__name__)
            print("Error message:", repr(error))
            print("===============================")

            logger.exception("PDF extraction failed")

            raise HTTPException(
                status_code=400,
                detail=f"{type(error).__name__}: {str(error)}"
            ) from error

    # 5. Extract TXT content
    else:

        try:
            text = file_content.decode("utf-8-sig")

        except UnicodeDecodeError as error:

            raise HTTPException(
                status_code=400,
                detail="TXT file must use UTF-8 encoding."
            ) from error

    # 6. Validate extracted text
    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail="No readable text found in the document."
        )

    return text


def save_document(file_content: bytes, filename: str):
    """
    Save uploaded document using a generated filename.
    """

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    extension = Path(filename).suffix.lower()

    saved_filename = f"{uuid4().hex}{extension}"

    file_path = UPLOAD_DIR / saved_filename

    file_path.write_bytes(file_content)

    return saved_filename
