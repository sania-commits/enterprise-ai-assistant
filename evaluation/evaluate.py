import json
from pathlib import Path

from agents.graph import agent_graph


TEST_CASES_PATH = Path("evaluation/test_cases.json")


def load_test_cases():
    """Load evaluation cases from JSON."""

    with open(TEST_CASES_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate():
    """Evaluate routing and answer correctness."""

    test_cases = load_test_cases()

    total = len(test_cases)
    route_correct = 0
    answer_correct = 0

    results = []

    for index, case in enumerate(test_cases, start=1):
        config = {
            "configurable": {
                "thread_id": f"evaluation-{index}"
            }
        }

        result = agent_graph.invoke(
            {
                "question": case["question"],
                "route": "",
                "answer": "",
                "sources": [],
                "history": [],
            },
            config=config,
        )

        route_match = (
            result["route"] == case["expected_route"]
        )

        keyword_match = (
            case["expected_keyword"].lower()
            in result["answer"].lower()
        )

        route_correct += int(route_match)
        answer_correct += int(keyword_match)

        results.append(
            {
                "question": case["question"],
                "expected_route": case["expected_route"],
                "actual_route": result["route"],
                "route_correct": route_match,
                "keyword_correct": keyword_match,
            }
        )

    print("\n--- EVALUATION RESULTS ---")

    for result in results:
        print(result)

    print("\n--- SUMMARY ---")
    print(
        f"Routing Accuracy: "
        f"{route_correct / total:.2%}"
    )
    print(
        f"Answer Keyword Accuracy: "
        f"{answer_correct / total:.2%}"
    )


if __name__ == "__main__":
    evaluate()
