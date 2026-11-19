
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GEMINI_API_KEY


# Initialize Gemini chat model

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=GEMINI_API_KEY,
    timeout=120,
    max_retries=1
)




import logging

logger = logging.getLogger(__name__)


def generate_answer(question: str, retrieved_chunks: list[dict]):

    if not retrieved_chunks:
        return "I couldn't find relevant information in the uploaded documents."

    context = "\n\n".join(
        chunk["content"] for chunk in retrieved_chunks
    )

    prompt = f"""
    You are a helpful document question-answering assistant.

    Answer the user's question using ONLY the provided context.

    If the answer is not available in the context,
    clearly say that the uploaded documents do not contain
    enough information to answer the question.

    Do not make up information.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    try:
        response = llm.invoke(prompt)

        if isinstance(response.content, str):
            return response.content

        return "\n".join(
            block["text"]
            for block in response.content
            if isinstance(block, dict) and block.get("type") == "text"
        )

    except Exception as error:
        logger.exception("Gemini answer generation failed")

        raise RuntimeError(
            "Unable to generate an answer using the AI service."
        ) from error
