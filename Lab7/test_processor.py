from hypothesis import given, strategies as st
import pytest
from processor import lookup_drink_code, calculate_average_shot_cost, parse_order_modifiers

# Comprehensive fuzzing strategy covering text, None, integers, floats, booleans, and lists
fuzz_input = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.booleans(),
    st.lists(st.text(), max_size=5)
)


# ======================================================================
# Hypothesis Property-Based Fuzz Tests
# ======================================================================

@given(fuzz_input)
def test_lookup_drink_code_no_crash(s):
    """
    Property: For any arbitrary input, lookup_drink_code must not crash with
    unhandled exceptions (KeyError, AttributeError, TypeError).
    It must return either a positive float price or None for invalid codes.
    """
    result = lookup_drink_code(s)
    if result is not None:
        assert isinstance(result, (int, float)), f"Expected numeric price, got {type(result)}"
        assert result > 0, f"Expected positive price, got {result}"


@given(fuzz_input)
def test_calculate_average_shot_cost_safe(s):
    """
    Property: For any arbitrary input, calculate_average_shot_cost must safely return
    a non-negative float average (0.0 when invalid) without crashing on malformed CSV,
    empty strings, None, or ZeroDivisionError.
    """
    result = calculate_average_shot_cost(s)
    assert isinstance(result, (int, float)), f"Expected numeric average, got {type(result)}"
    assert result >= 0.0, f"Expected non-negative average, got {result}"


@given(fuzz_input)
def test_parse_order_modifiers_safe(s):
    """
    Property: For any arbitrary input, parse_order_modifiers must safely return
    a dictionary without crashing on None, missing colons, multiple colons,
    or malformed delimiters.
    """
    result = parse_order_modifiers(s)
    assert isinstance(result, dict), f"Expected dict, got {type(result)}"


# ======================================================================
# Deterministic Functional & Edge-Case Tests
# ======================================================================

def test_lookup_drink_code_valid():
    """Verify normal valid menu drink code lookups."""
    assert lookup_drink_code("LAT") == 4.50
    assert lookup_drink_code("CAP") == 4.00
    assert lookup_drink_code("ESP") == 3.00
    assert lookup_drink_code("AME") == 3.50
    assert lookup_drink_code("MOC") == 5.00


def test_lookup_drink_code_case_and_padding():
    """Verify case insensitivity and extra suffix handling."""
    assert lookup_drink_code("latte") == 4.50
    assert lookup_drink_code("cap_extra") == 4.00
    assert lookup_drink_code("  esp  ") == 3.00


def test_lookup_drink_code_invalid():
    """Verify safe fallback for unknown, empty, or short codes."""
    assert lookup_drink_code("XYZ") is None
    assert lookup_drink_code("") is None
    assert lookup_drink_code("AB") is None
    assert lookup_drink_code(None) is None


def test_calculate_average_shot_cost_normal():
    """Verify average calculation for standard CSV input."""
    assert calculate_average_shot_cost("1.0, 1.5, 2.0") == 1.50
    assert calculate_average_shot_cost("2.50") == 2.50


def test_calculate_average_shot_cost_robustness():
    """Verify defensive handling of empty, whitespace, and malformed inputs."""
    assert calculate_average_shot_cost("") == 0.0
    assert calculate_average_shot_cost(None) == 0.0
    assert calculate_average_shot_cost("abc, def") == 0.0
    assert calculate_average_shot_cost("1.0, -2.0, 3.0") == 2.00  # Skips negative value


def test_parse_order_modifiers_normal():
    """Verify parsing standard semicolon-separated modifiers."""
    spec = "milk:oat;syrup:vanilla;temp:extra_hot"
    expected = {"milk": "oat", "syrup": "vanilla", "temp": "extra_hot"}
    assert parse_order_modifiers(spec) == expected


def test_parse_order_modifiers_edge_cases():
    """Verify handling of empty strings, None, trailing semicolons, and missing colons."""
    assert parse_order_modifiers("") == {}
    assert parse_order_modifiers(None) == {}
    assert parse_order_modifiers("milk:oat;") == {"milk": "oat"}
    assert parse_order_modifiers("invalid_entry;sugar:2") == {"sugar": "2"}
    assert parse_order_modifiers("extra:shot:special") == {"extra": "shot:special"}
