import json
from pathlib import Path

from rag.rag_chain import ask_documents


DATASET_PATH = Path(
    "evaluation/groundedness_cases.json"
)


def load_cases():
    """Load groundedness evaluation cases."""

    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def evaluate_groundedness():
    """Evaluate grounded RAG responses."""

    cases = load_cases()

    correct = 0
    hallucinations = 0

    for index, case in enumerate(cases, start=1):
        answer, documents = ask_documents(
            case["question"]
        )

        # Check whether the expected factual keyword
        # appears in the generated answer.
        keyword_found = (
            case["expected_keyword"].lower()
            in answer.lower()
        )

        # Our RAG chain is instructed to use this phrase
        # when the documents do not contain enough information.
        refusal_phrase = (
            "don't have enough information"
        )

        proper_refusal = (
            refusal_phrase in answer.lower()
        )

        # Answerable questions should contain
        # the expected factual information.
        if case["answerable"]:
            case_passed = keyword_found

        # Unanswerable questions should produce
        # the required grounded refusal.
        else:
            case_passed = proper_refusal

            if not proper_refusal:
                hallucinations += 1

        if case_passed:
            correct += 1

        print(f"\nCase {index}")
        print(f"Question: {case['question']}")
        print(f"Answerable: {case['answerable']}")
        print(f"Answer: {answer}")
        print(f"Passed: {case_passed}")

        sources = [
            document.metadata.get(
                "source",
                "unknown",
            )
            for document in documents
        ]

        print(f"Sources: {sources}")

    total = len(cases)

    accuracy = (
        correct / total
        if total
        else 0
    )

    unanswerable_count = sum(
        not case["answerable"]
        for case in cases
    )

    hallucination_rate = (
        hallucinations / unanswerable_count
        if unanswerable_count
        else 0
    )

    print("\n--- GROUNDEDNESS SUMMARY ---")

    print(
        f"Groundedness Accuracy: "
        f"{accuracy:.2%}"
    )

    print(
        f"Hallucination Rate: "
        f"{hallucination_rate:.2%}"
    )


if __name__ == "__main__":
    evaluate_groundedness()