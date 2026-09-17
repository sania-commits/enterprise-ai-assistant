from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


@patch("backend.main.agent_graph.invoke")
def test_ask_endpoint_passes_thread_id(mock_invoke):
    mock_invoke.return_value = {
        "answer": "Employees receive 24 annual leave days.",
        "route": "rag",
        "sources": [
            "data/raw/employee_handbook.txt"
        ],
        "history": [],
    }

    response = client.post(
        "/ask",
        json={
            "question": (
                "How many annual leave days "
                "do employees receive?"
            ),
            "thread_id": "test-thread-123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["route"] == "rag"
    assert "24" in data["answer"]

    mock_invoke.assert_called_once()

    args, kwargs = mock_invoke.call_args

    state = args[0]
    config = kwargs["config"]

    assert state["question"] == (
        "How many annual leave days "
        "do employees receive?"
    )

    assert state["history"] == []

    assert (
        config["configurable"]["thread_id"]
        == "test-thread-123"
    )

def test_ask_endpoint_requires_thread_id():
    response = client.post(
        "/ask",
        json={
            "question": "What is the remote work policy?"
        },
    )

    assert response.status_code == 422


def test_ask_endpoint_rejects_short_question():
    response = client.post(
        "/ask",
        json={
            "question": "Hi",
            "thread_id": "test-thread-123",
        },
    )

    assert response.status_code == 422
