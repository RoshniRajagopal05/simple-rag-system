import pytest
from pydantic import ValidationError

from app.schemas.question import QuestionRequest


def test_valid_question():
    request = QuestionRequest(question="What is Django?")

    assert request.question == "What is Django?"
    assert request.document_id is None


def test_question_whitespace_is_removed():
    request = QuestionRequest(question="  What is Django?  ")

    assert request.question == "What is Django?"


def test_reject_empty_question():
    with pytest.raises(ValidationError):
        QuestionRequest(question="")


def test_reject_whitespace_question():
    with pytest.raises(ValidationError):
        QuestionRequest(question="     ")


def test_reject_question_longer_than_limit():
    with pytest.raises(ValidationError):
        QuestionRequest(question="A" * 1001)


def test_document_id_is_optional():
    request = QuestionRequest(question="Explain Python")

    assert request.document_id is None