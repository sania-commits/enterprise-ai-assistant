from typing import Annotated, TypedDict
import operator


class AgentState(TypedDict):
    question: str
    route: str
    answer: str
    sources: list[str]

    history: Annotated[list[str], operator.add]
