
from io import BytesIO

import pytest
from fastapi import HTTPException
from pypdf import PdfWriter

from app.services.document_service import extract_document


def test_extract_txt_file():
    content = b"Python is a programming language."

    result = extract_document(
        file_content=content,
        filename="notes.txt"
    )

    assert result == "Python is a programming language."


def test_extract_empty_file():
    with pytest.raises(HTTPException) as exc_info:
        extract_document(
            file_content=b"",
            filename="empty.txt"
        )

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Uploaded file is empty."


def test_reject_unsupported_file():
    with pytest.raises(HTTPException) as exc_info:
        extract_document(
            file_content=b"Some content",
            filename="notes.docx"
        )

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Only PDF and TXT files are supported."


def test_reject_invalid_txt_encoding():
    with pytest.raises(HTTPException) as exc_info:
        extract_document(
            file_content=b"\xff\xfe\xfa",
            filename="notes.txt"
        )

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "TXT file must use UTF-8 encoding."


def test_extract_blank_pdf():
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)

    pdf_buffer = BytesIO()
    writer.write(pdf_buffer)

    with pytest.raises(HTTPException) as exc_info:
        extract_document(
            file_content=pdf_buffer.getvalue(),
            filename="blank.pdf"
        )

    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == "No readable text found in the document."
