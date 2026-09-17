from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        description="Question to ask the enterprise AI assistant",
    )

    thread_id: str = Field(
        ...,
        min_length=1,
        description="Unique conversation thread identifier",
    )


class AskResponse(BaseModel):
    answer: str
    route: str
    sources: list[str]