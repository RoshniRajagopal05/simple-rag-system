
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)

request_data = {
    "question": "Which Python framework can be used for web development?",
    "document_id": "2297b127-f630-491c-86fa-ecb5782580b2"
}

print("Testing simulated Gemini failure...")

with patch(
    "app.routes.questions.generate_answer",
    side_effect=RuntimeError("Simulated Gemini API failure")
):
    response = client.post(
        "/questions/ask/",
        json=request_data
    )

print("\nStatus Code:", response.status_code)
print("Response:", response.json())

assert response.status_code == 503

print("\nGemini error handling test passed!")
