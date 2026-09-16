from langgraph.graph import END, START, StateGraph

from agents.nodes import calculator_node, general_node, rag_node
from agents.router import router_node
from agents.state import AgentState


def route_question(state: AgentState):
    """Return the route selected by the router node."""

    return state["route"]


def build_agent_graph():
    """Build and compile the enterprise AI assistant graph."""

    builder = StateGraph(AgentState)

    # Add nodes
    builder.add_node("router", router_node)
    builder.add_node("rag", rag_node)
    builder.add_node("general", general_node)
    builder.add_node("calculator", calculator_node)

    # Start with the router
    builder.add_edge(START, "router")

    # Route conditionally
    builder.add_conditional_edges(
        "router",
        route_question,
        {
            "rag": "rag",
            "calculator": "calculator",
            "general": "general",
        },
    )

    # Finish after either answering path
    builder.add_edge("rag", END)
    builder.add_edge("calculator", END)
    builder.add_edge("general", END)

    return builder.compile()


agent_graph = build_agent_graph()
