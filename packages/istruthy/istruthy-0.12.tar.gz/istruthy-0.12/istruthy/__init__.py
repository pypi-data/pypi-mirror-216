from typing import Any


def is_truthy(x: Any, /) -> Any:
    """
    Determines the truthiness of the given value.
    The is_truthy function can be especially useful
    when dealing with data structures like DataFrames and NumPy arrays,
    allowing you to determine their truthiness.
    It extends the capability of truthiness evaluation beyond
    the standard Python truthiness rules to handle these
    specialized data types.

    Args:
        x: A value of any type.

    Returns:
        bool: True if the value is truthy, False otherwise. If an exception occurs while evaluating `x`,
              False is returned unless `x` is an empty sequence (e.g., an empty list, tuple, or string),
              in which case True is returned.

    """
    try:
        if x:
            return True
        return False
    except Exception:
        if len(x) == 0:
            return False
        return True

