import json
from pathlib import Path


TEST_CASES_PATH = Path("evaluation/test_cases.json")

VALID_ROUTES = {
    "rag",
    "calculator",
    "general",
}


def load_test_cases():
    with open(
        TEST_CASES_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def test_evaluation_dataset_exists():
    assert TEST_CASES_PATH.exists()


def test_evaluation_dataset_not_empty():
    test_cases = load_test_cases()

    assert len(test_cases) > 0


def test_required_fields_exist():
    test_cases = load_test_cases()

    required_fields = {
        "question",
        "expected_route",
        "expected_keyword",
    }

    for case in test_cases:
        assert required_fields.issubset(case.keys())


def test_expected_routes_are_valid():
    test_cases = load_test_cases()

    for case in test_cases:
        assert case["expected_route"] in VALID_ROUTES


def test_questions_are_not_empty():
    test_cases = load_test_cases()

    for case in test_cases:
        assert case["question"].strip()

GROUNDEDNESS_PATH = Path(
    "evaluation/groundedness_cases.json"
)


def test_groundedness_dataset():
    assert GROUNDEDNESS_PATH.exists()

    with open(
        GROUNDEDNESS_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        cases = json.load(file)

    assert len(cases) > 0

    for case in cases:
        assert "question" in case
        assert "answerable" in case
        assert "expected_keyword" in case

        assert isinstance(
            case["answerable"],
            bool,
        )
