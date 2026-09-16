from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        description="Question to ask the enterprise knowledge base",
    )


class AskResponse(BaseModel):
    answer: str
    route: str
    sources: list[str]
