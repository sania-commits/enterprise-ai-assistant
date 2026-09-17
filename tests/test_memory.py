from typing import Annotated, TypedDict
import operator

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph


class TestState(TypedDict):
    history: Annotated[list[str], operator.add]


def add_message(state: TestState):
    return {
        "history": ["New message"]
    }


def build_test_graph():
    builder = StateGraph(TestState)

    builder.add_node("add_message", add_message)

    builder.add_edge(START, "add_message")
    builder.add_edge("add_message", END)

    memory = InMemorySaver()

    return builder.compile(checkpointer=memory)


def test_memory_persists_between_turns():
    graph = build_test_graph()

    config = {
        "configurable": {
            "thread_id": "test-thread"
        }
    }

    first = graph.invoke(
        {"history": []},
        config=config,
    )

    second = graph.invoke(
        {"history": []},
        config=config,
    )

    assert len(first["history"]) == 1
    assert len(second["history"]) == 2
