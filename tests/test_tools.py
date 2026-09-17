from agents.tools import calculator


def test_basic_multiplication():
    result = calculator.invoke(
        {"expression": "2500 * 0.18"}
    )

    assert result == "450.0"


def test_parentheses():
    result = calculator.invoke(
        {"expression": "(100 + 50) / 3"}
    )

    assert result == "50.0"


def test_power():
    result = calculator.invoke(
        {"expression": "2 ** 8"}
    )

    assert result == "256"


def test_modulo():
    result = calculator.invoke(
        {"expression": "10 % 3"}
    )

    assert result == "1"


def test_division_by_zero():
    result = calculator.invoke(
        {"expression": "10 / 0"}
    )

    assert result == (
        "Unable to calculate the expression."
    )


def test_rejects_python_code():
    result = calculator.invoke(
        {"expression": "__import__('os')"}
    )

    assert result == (
        "Unable to calculate the expression."
    )


def test_rejects_variable_names():
    result = calculator.invoke(
        {"expression": "x + 10"}
    )

    assert result == (
        "Unable to calculate the expression."
    )


def test_rejects_large_exponent():
    result = calculator.invoke(
        {"expression": "2 ** 1000000"}
    )

    assert result == (
        "Unable to calculate the expression."
    )


def test_rejects_extremely_large_result():
    result = calculator.invoke(
        {"expression": "10 ** 101"}
    )

    assert result == (
        "Unable to calculate the expression."
    )


def test_rejects_long_expression():
    expression = "1+" * 101 + "1"

    result = calculator.invoke(
        {"expression": expression}
    )

    assert result == (
        "Unable to calculate the expression."
    )