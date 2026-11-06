from hypothesis import given, strategies as st
import pytest
from processor import lookup_drink_code, calculate_average_shot_cost, parse_order_modifiers

# Fuzzing strategy covering text, None, numbers, booleans, and collections
fuzz_input = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.booleans(),
    st.lists(st.text(), max_size=5)
)


@given(fuzz_input)
def test_lookup_drink_code_no_crash(s):
    """
    Test lookup_drink_code with arbitrary fuzz inputs.
    A hardened implementation should either return a valid positive price float
    or None/safe fallback for invalid codes without unhandled crashes (KeyError, AttributeError).
    """
    result = lookup_drink_code(s)
    if result is not None:
        assert isinstance(result, (int, float)), f"Expected numeric price, got {type(result)}"
        assert result > 0, f"Expected positive price, got {result}"


@given(fuzz_input)
def test_calculate_average_shot_cost_safe(s):
    """
    Test calculate_average_shot_cost with arbitrary fuzz inputs.
    A hardened implementation must safely return a non-negative float average (or 0.0)
    without crashing on empty strings, None, malformed CSV, or ZeroDivisionError.
    """
    result = calculate_average_shot_cost(s)
    assert isinstance(result, (int, float)), f"Expected numeric average, got {type(result)}"
    assert result >= 0.0, f"Expected non-negative average, got {result}"


@given(fuzz_input)
def test_parse_order_modifiers_safe(s):
    """
    Test parse_order_modifiers with arbitrary fuzz inputs.
    A hardened implementation must return a dictionary of parsed modifiers
    without crashing on None, missing colons, multiple colons, or empty strings.
    """
    result = parse_order_modifiers(s)
    assert isinstance(result, dict), f"Expected dict, got {type(result)}"
