
from app.services.generation_service import generate_answer

question = "Which Python framework can be used for web development?"

retrieved_chunks = [
    {
        "content": "Django is a Python framework used for web development.",
        "metadata": {
            "filename": "python_notes.txt"
        }
    }
]

print("Starting Gemini answer generation...", flush=True)

try:
    answer = generate_answer(
        question=question,
        retrieved_chunks=retrieved_chunks
    )

    print("\nQuestion:", question)
    print("\nGenerated Answer:")
    print(answer)

except Exception as error:
    print("\nGemini request failed!")
    print("Error type:", type(error).__name__)
    print("Error details:", str(error))
