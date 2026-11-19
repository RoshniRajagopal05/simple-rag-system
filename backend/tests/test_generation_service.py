
from unittest.mock import patch, MagicMock

import pytest

from app.services.generation_service import generate_answer


def test_generate_answer_success():

    retrieved_chunks = [
        {
            "content": "Django is a Python web framework.",
            "metadata": {"filename": "python.txt"}
        }
    ]

    mock_response = MagicMock()
    mock_response.content = "Django is a Python web framework."

    with patch(
        "app.services.generation_service.llm"
    ) as mock_llm:

        mock_llm.invoke.return_value = mock_response

        answer = generate_answer(
            question="What is Django?",
            retrieved_chunks=retrieved_chunks
        )

    assert answer == "Django is a Python web framework."
    mock_llm.invoke.assert_called_once()


def test_generate_answer_no_chunks():

    answer = generate_answer(
        question="What is Django?",
        retrieved_chunks=[]
    )

    assert answer == "I couldn't find relevant information in the uploaded documents."


def test_generate_answer_failure():

    retrieved_chunks = [
        {
            "content": "Django is a Python web framework.",
            "metadata": {"filename": "python.txt"}
        }
    ]

    with patch(
        "app.services.generation_service.llm"
    ) as mock_llm:

        mock_llm.invoke.side_effect = Exception(
            "Simulated Gemini failure"
        )

        with pytest.raises(
            RuntimeError,
            match="Unable to generate an answer using the AI service."
        ):
            generate_answer(
                question="What is Django?",
                retrieved_chunks=retrieved_chunks
            )
