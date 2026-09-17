from unittest.mock import MagicMock, patch

from agents.router import router_node


@patch("agents.router.get_llm")
def test_router_uses_only_recent_history(mock_get_llm):
    """Router should include only the latest six history entries."""

    llm = MagicMock()
    llm.invoke.return_value = MagicMock(
        content="rag"
    )
    mock_get_llm.return_value = llm

    history = [
        "OLD_HISTORY_ENTRY",
        "History 2",
        "History 3",
        "History 4",
        "History 5",
        "History 6",
        "LATEST_HISTORY_ENTRY",
    ]

    state = {
        "question": "What is the remote work policy?",
        "history": history,
    }

    result = router_node(state)

    prompt = llm.invoke.call_args[0][0]

    assert "OLD_HISTORY_ENTRY" not in prompt
    assert "History 2" in prompt
    assert "LATEST_HISTORY_ENTRY" in prompt
    assert result["route"] == "rag"


@patch("agents.router.get_llm")
def test_router_preserves_valid_calculator_route(
    mock_get_llm,
):
    """Router should preserve a valid calculator route."""

    llm = MagicMock()
    llm.invoke.return_value = MagicMock(
        content="calculator"
    )
    mock_get_llm.return_value = llm

    state = {
        "question": "What is 25 * 4?",
        "history": [],
    }

    result = router_node(state)

    assert result["route"] == "calculator"


@patch("agents.router.get_llm")
def test_router_falls_back_to_general(
    mock_get_llm,
):
    """Invalid model output should safely use general."""

    llm = MagicMock()
    llm.invoke.return_value = MagicMock(
        content="something-invalid"
    )
    mock_get_llm.return_value = llm

    state = {
        "question": "Explain machine learning.",
        "history": [],
    }

    result = router_node(state)

    assert result["route"] == "general"
