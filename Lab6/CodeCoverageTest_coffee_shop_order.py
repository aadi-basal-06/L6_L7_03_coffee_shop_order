import pytest
from coffee_shop_order import process_order_batch, check_espresso_machine


# ----------------------------------------------------------------------
# Tests for process_order_batch
# ----------------------------------------------------------------------

def test_invalid_orders_type():
    """Verify ValueError is raised if orders is not a list."""
    with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
        process_order_batch("not a list", 0.05)


def test_invalid_negative_tax_rate():
    """Verify ValueError is raised if tax_rate is negative."""
    with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
        process_order_batch([], -0.01)


def test_empty_orders_no_sale():
    """Verify empty orders list returns NO_SALE status with 0.0 total."""
    result = process_order_batch([], 0.08)
    assert result == {"total": 0.0, "status": "NO_SALE"}


def test_unpaid_order_skipped():
    """Verify unpaid orders are ignored and return NO_SALE if all unpaid."""
    orders = [{"paid": False, "size": "medium"}]
    result = process_order_batch(orders, 0.10)
    assert result == {"total": 0.0, "status": "NO_SALE"}


def test_size_small():
    """Verify base price calculation for small size."""
    orders = [{"paid": True, "size": "small"}]
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 3.0, "status": "COMPLETED"}


def test_size_medium_default():
    """Verify default medium size calculation."""
    orders = [{"paid": True}]
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 4.5, "status": "COMPLETED"}


def test_size_large():
    """Verify base price calculation for large size."""
    orders = [{"paid": True, "size": "large"}]
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 6.0, "status": "COMPLETED"}


def test_unknown_size_rejected():
    """Verify unrecognized drink size increments rejected_items and is skipped."""
    orders = [{"paid": True, "size": "extra_large"}]
    result = process_order_batch(orders, 0.05)
    assert result == {"total": 0.0, "status": "NO_SALE"}


def test_customization_negative_cost():
    """Verify customization with negative cost is rejected and skipped."""
    orders = [
        {
            "paid": True,
            "size": "medium",
            "customizations": [{"type": "caramel", "cost": -1.0}]
        }
    ]
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 4.5, "status": "COMPLETED"}


def test_customization_allergen_alert_strict():
    """Verify allergen_alert with strict_allergy clears item total and breaks."""
    orders = [
        {
            "paid": True,
            "size": "medium",
            "strict_allergy": True,
            "customizations": [
                {"type": "allergen_alert", "cost": 0.0},
                {"type": "extra_shot", "cost": 1.0}
            ]
        }
    ]
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 0.0, "status": "NO_SALE"}


def test_customization_allergen_alert_non_strict():
    """Verify allergen_alert without strict allergy keeps item base price."""
    orders = [
        {
            "paid": True,
            "size": "small",
            "strict_allergy": False,
            "customizations": [{"type": "allergen_alert", "cost": 0.0}]
        }
    ]
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 3.0, "status": "COMPLETED"}


def test_customization_syrup_cap():
    """Verify syrup cost capping at 1.5."""
    orders_normal_syrup = [
        {
            "paid": True,
            "size": "small",
            "customizations": [{"type": "syrup", "cost": 0.75}]
        }
    ]
    result_normal = process_order_batch(orders_normal_syrup, 0.0)
    assert result_normal["total"] == 3.75

    orders_expensive_syrup = [
        {
            "paid": True,
            "size": "small",
            "customizations": [{"type": "syrup", "cost": 2.50}]
        }
    ]
    result_expensive = process_order_batch(orders_expensive_syrup, 0.0)
    assert result_expensive["total"] == 4.50


def test_customization_standard_addon():
    """Verify non-syrup customizations are added directly."""
    orders = [
        {
            "paid": True,
            "size": "small",
            "customizations": [{"type": "oat_milk", "cost": 0.80}]
        }
    ]
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 3.80, "status": "COMPLETED"}


def test_member_discount():
    """Verify 10% discount is applied to members."""
    orders = [
        {
            "paid": True,
            "size": "large",
            "is_member": True
        }
    ]
    # base 6.0 * 0.9 = 5.40, with 10% tax = 5.94
    result = process_order_batch(orders, 0.10)
    assert result == {"total": 5.94, "status": "COMPLETED"}


def test_audit_rejected_status():
    """Verify AUDIT_REJECTED status when rejected items exceed 4."""
    orders = [
        {"paid": True, "size": "invalid1"},
        {"paid": True, "size": "invalid2"},
        {"paid": True, "size": "invalid3"},
        {"paid": True, "size": "invalid4"},
        {"paid": True, "size": "invalid5"},
        {"paid": True, "size": "small"}
    ]
    result = process_order_batch(orders, 0.10)
    assert result["status"] == "AUDIT_REJECTED"
    assert result["total"] == 3.30


# ----------------------------------------------------------------------
# Tests for check_espresso_machine
# ----------------------------------------------------------------------

def test_espresso_no_data():
    """Verify NO_DATA returned for empty temperature cycles."""
    assert check_espresso_machine([]) == "NO_DATA"
    assert check_espresso_machine(None) == "NO_DATA"


def test_espresso_shutdown():
    """Verify SHUTDOWN returned when two consecutive readings exceed 96.0."""
    cycles = [
        [94.0, 95.0],
        [96.5, 97.2, 92.0]
    ]
    assert check_espresso_machine(cycles) == "SHUTDOWN"


def test_espresso_streak_resets_optimal():
    """Verify overheat streak resets when reading drops to or below 96.0."""
    cycles = [
        [97.0, 95.0, 97.0],
        [96.0, 93.5]
    ]
    assert check_espresso_machine(cycles) == "OPTIMAL"

