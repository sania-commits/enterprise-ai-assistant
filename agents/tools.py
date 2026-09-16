from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """Calculate a basic mathematical expression."""

    allowed_characters = set(
        "0123456789+-*/(). %"
    )

    if not set(expression).issubset(allowed_characters):
        return "Invalid mathematical expression."

    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            {},
        )

        return str(result)

    except Exception:
        return "Unable to calculate the expression."
