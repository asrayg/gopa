"""Builtin standard library functions for Gopa."""

import random
import math
from typing import List, Any, Callable


def builtin_random() -> float:
    """Returns a random number between 0 and 1."""
    return random.random()


def builtin_random_int(min_val: int, max_val: int) -> int:
    """Returns a random integer between min and max (inclusive)."""
    return random.randint(min_val, max_val)


def builtin_floor(x: float) -> int:
    """Returns the floor of x."""
    return math.floor(x)


def builtin_ceil(x: float) -> int:
    """Returns the ceiling of x."""
    return math.ceil(x)


def builtin_round(x: float) -> int:
    """Returns the rounded value of x."""
    return round(x)


def builtin_abs(x: float) -> float:
    """Returns the absolute value of x."""
    return abs(x)


def builtin_sqrt(x: float) -> float:
    """Returns the square root of x."""
    return math.sqrt(x)


def builtin_sin(x: float) -> float:
    """Returns the sine of x (in radians)."""
    return math.sin(x)


def builtin_cos(x: float) -> float:
    """Returns the cosine of x (in radians)."""
    return math.cos(x)


def builtin_tan(x: float) -> float:
    """Returns the tangent of x (in radians)."""
    return math.tan(x)


def builtin_pow(base: float, exp: float) -> float:
    """Returns base raised to the power of exp."""
    return math.pow(base, exp)


def builtin_log(x: float) -> float:
    """Returns the natural logarithm of x."""
    return math.log(x)


def builtin_max(values: List[Any]) -> Any:
    """Returns the maximum value in a list."""
    if not values:
        return None
    return max(values)


def builtin_min(values: List[Any]) -> Any:
    """Returns the minimum value in a list."""
    if not values:
        return None
    return min(values)


def builtin_sum(values: List[float]) -> float:
    """Returns the sum of values in a list."""
    return sum(values)


def builtin_len(value: Any) -> int:
    """Returns the length of a string, list, or dictionary."""
    if isinstance(value, str):
        return len(value)
    elif isinstance(value, list):
        return len(value)
    elif isinstance(value, dict):
        return len(value)
    else:
        raise TypeError(f"Cannot get length of {type(value)}")


def builtin_range(start: int, end: int) -> List[int]:
    """Returns a list of integers from start to end (exclusive)."""
    return list(range(start, end))


def builtin_type_of(value: Any) -> str:
    """Returns the type name of a value."""
    if value is None:
        return "nothing"
    elif isinstance(value, bool):
        return "boolean"
    elif isinstance(value, (int, float)):
        return "number"
    elif isinstance(value, str):
        return "string"
    elif isinstance(value, list):
        return "list"
    elif isinstance(value, dict):
        return "dictionary"
    else:
        return "object"


def builtin_to_string(value: Any) -> str:
    """Converts a value to a string."""
    if value is None:
        return ""
    return str(value)


def builtin_to_number(value: Any) -> float:
    """Converts a value to a number."""
    if isinstance(value, (int, float)):
        return float(value)
    elif isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return 0.0
    elif isinstance(value, bool):
        return 1.0 if value else 0.0
    else:
        return 0.0


def builtin_print_table(headers: List[str], rows: List[List[Any]]) -> str:
    """Prints a formatted table."""
    if not rows:
        return ""
    
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))
    
    lines = []
    
    header_line = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    lines.append(header_line)
    lines.append("-" * len(header_line))
    
    for row in rows:
        row_line = " | ".join(str(row[i] if i < len(row) else "").ljust(col_widths[i]) 
                             for i in range(len(headers)))
        lines.append(row_line)
    
    return "\n".join(lines)


BUILTINS = {
    "random": builtin_random,
    "random_int": builtin_random_int,
    "floor": builtin_floor,
    "ceil": builtin_ceil,
    "round": builtin_round,
    "abs": builtin_abs,
    "sqrt": builtin_sqrt,
    "sin": builtin_sin,
    "cos": builtin_cos,
    "tan": builtin_tan,
    "pow": builtin_pow,
    "log": builtin_log,
    "max": builtin_max,
    "min": builtin_min,
    "sum": builtin_sum,
    "len": builtin_len,
    "range": builtin_range,
    "type_of": builtin_type_of,
    "to_string": builtin_to_string,
    "to_number": builtin_to_number,
    "print_table": builtin_print_table,
}

