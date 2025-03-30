from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(
        description="The question to be asked", default="Quando começam as aulas?"
    )
    chat_id: str = Field(
        description="The chat ID to which the question belongs", default="123456789"
    )
