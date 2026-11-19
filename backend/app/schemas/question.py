from pydantic import BaseModel, Field, field_validator


class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=1000,
        description="Question about the uploaded documents"
    )

    document_id: str | None = Field(
        default=None,
        description="Optional document ID to restrict the search"
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value):
        if not value.strip():
            raise ValueError("Question cannot contain only whitespace.")
        return value.strip()