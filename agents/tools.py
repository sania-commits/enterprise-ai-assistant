import ast
import operator

from langchain_core.tools import tool


BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def evaluate_expression(node):
    """Safely evaluate supported arithmetic AST nodes."""

    if isinstance(node, ast.Expression):
        return evaluate_expression(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError(
            "Only numbers are allowed."
        )

    if isinstance(node, ast.BinOp):
        operator_function = BINARY_OPERATORS.get(
            type(node.op)
        )

        if operator_function is None:
            raise ValueError(
                "Unsupported mathematical operator."
            )

        left = evaluate_expression(node.left)
        right = evaluate_expression(node.right)

        return operator_function(
            left,
            right,
        )

    if isinstance(node, ast.UnaryOp):
        operator_function = UNARY_OPERATORS.get(
            type(node.op)
        )

        if operator_function is None:
            raise ValueError(
                "Unsupported unary operator."
            )

        operand = evaluate_expression(
            node.operand
        )

        return operator_function(
            operand
        )

    raise ValueError(
        "Unsupported mathematical expression."
    )


@tool
def calculator(expression: str) -> str:
    """Calculate a basic mathematical expression safely."""

    try:
        parsed_expression = ast.parse(
            expression,
            mode="eval",
        )

        result = evaluate_expression(
            parsed_expression
        )

        return str(result)

    except (
        SyntaxError,
        ValueError,
        TypeError,
        ZeroDivisionError,
        OverflowError,
    ):
        return "Unable to calculate the expression."