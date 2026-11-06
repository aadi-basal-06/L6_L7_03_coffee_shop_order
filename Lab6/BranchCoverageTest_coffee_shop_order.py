import pytest
from coffee_shop_order import process_order_batch, check_espresso_machine


# ======================================================================
# Branch Coverage Suite for process_order_batch
# ======================================================================

def test_branch_input_validation_non_list():
    """Branch: not isinstance(orders, list) -> True."""
    with pytest.raises(ValueError):
        process_order_batch({"order": 1}, 0.05)


def test_branch_input_validation_negative_tax():
    """Branch: not isinstance(orders, list) -> False, tax_rate < 0 -> True."""
    with pytest.raises(ValueError):
        process_order_batch([], -0.05)


def test_branch_empty_order_list_no_sale():
    """Branch: orders loop zero iterations, batch_total == 0.0 -> True."""
    result = process_order_batch([], 0.0)
    assert result["status"] == "NO_SALE"
    assert result["total"] == 0.0


def test_branch_order_unpaid_vs_paid():
    """Branch: not order.get('paid') -> True vs False."""
    orders = [
        {"paid": False, "size": "small"},
        {"paid": True, "size": "small"}
    ]
    result = process_order_batch(orders, 0.0)
    assert result["status"] == "COMPLETED"
    assert result["total"] == 3.0


def test_branch_size_evaluation_all_paths():
    """Branches: size == small, size == medium, size == large, size invalid."""
    orders = [
        {"paid": True, "size": "small"},       # base_price 3.0
        {"paid": True, "size": "medium"},      # base_price 4.5
        {"paid": True, "size": "large"},       # base_price 6.0
        {"paid": True, "size": "unknown_size"} # rejected_items += 1, continue
    ]
    # batch_total = 13.5
    result = process_order_batch(orders, 0.0)
    assert result["status"] == "COMPLETED"
    assert result["total"] == 13.5


def test_branch_customization_cost_negative_vs_positive():
    """Branch: cost < 0 -> True (reject mod) vs False (process mod)."""
    orders = [
        {
            "paid": True,
            "size": "small",
            "customizations": [
                {"type": "cinnamon", "cost": -0.50},  # negative cost branch
                {"type": "honey", "cost": 0.50}       # non-negative cost branch
            ]
        }
    ]
    result = process_order_batch(orders, 0.0)
    assert result["status"] == "COMPLETED"
    assert result["total"] == 3.50


def test_branch_allergen_alert_strict_true():
    """Branch: mod_type == allergen_alert -> True, strict_allergy -> True (break)."""
    orders = [
        {
            "paid": True,
            "size": "large",
            "strict_allergy": True,
            "customizations": [
                {"type": "allergen_alert", "cost": 0.0},
                {"type": "flavor", "cost": 1.0}  # Should not be reached due to break
            ]
        }
    ]
    result = process_order_batch(orders, 0.0)
    assert result["status"] == "NO_SALE"
    assert result["total"] == 0.0


def test_branch_allergen_alert_strict_false():
    """Branch: mod_type == allergen_alert -> True, strict_allergy -> False (no break)."""
    orders = [
        {
            "paid": True,
            "size": "small",
            "strict_allergy": False,
            "customizations": [
                {"type": "allergen_alert", "cost": 0.0},
                {"type": "flavor", "cost": 1.0}
            ]
        }
    ]
    result = process_order_batch(orders, 0.0)
    assert result["status"] == "COMPLETED"
    assert result["total"] == 4.0


def test_branch_syrup_cost_boundary():
    """Branch: mod_type == syrup -> cost <= 1.5 vs cost > 1.5."""
    orders = [
        {
            "paid": True,
            "size": "small",
            "customizations": [
                {"type": "syrup", "cost": 1.50},  # boundary at 1.5
                {"type": "syrup", "cost": 2.00}   # exceeds 1.5, capped to 1.5
            ]
        }
    ]
    # base 3.0 + 1.50 + 1.50 = 6.00
    result = process_order_batch(orders, 0.0)
    assert result["total"] == 6.00


def test_branch_member_discount_branching():
    """Branch: is_member -> True vs False."""
    orders_member = [{"paid": True, "size": "medium", "is_member": True}]
    orders_non_member = [{"paid": True, "size": "medium", "is_member": False}]

    res_member = process_order_batch(orders_member, 0.0)
    res_non_member = process_order_batch(orders_non_member, 0.0)

    assert res_member["total"] == 4.05      # 4.5 * 0.90
    assert res_non_member["total"] == 4.50  # 4.5 * 1.0


def test_branch_audit_rejected_threshold():
    """Branch: rejected_items > 4 -> True vs False."""
    # 5 rejected items triggers AUDIT_REJECTED
    orders_audit = [
        {"paid": True, "size": "bad1"},
        {"paid": True, "size": "bad2"},
        {"paid": True, "size": "bad3"},
        {"paid": True, "size": "bad4"},
        {"paid": True, "size": "bad5"},
        {"paid": True, "size": "small"}
    ]
    res_audit = process_order_batch(orders_audit, 0.0)
    assert res_audit["status"] == "AUDIT_REJECTED"

    # Exactly 4 rejected items does NOT trigger AUDIT_REJECTED (> 4 required)
    orders_not_audit = [
        {"paid": True, "size": "bad1"},
        {"paid": True, "size": "bad2"},
        {"paid": True, "size": "bad3"},
        {"paid": True, "size": "bad4"},
        {"paid": True, "size": "small"}
    ]
    res_not_audit = process_order_batch(orders_not_audit, 0.0)
    assert res_not_audit["status"] == "COMPLETED"


# ======================================================================
# Branch Coverage Suite for check_espresso_machine
# ======================================================================

def test_branch_espresso_falsy_cycles():
    """Branch: not temperature_cycles -> True (empty list & None)."""
    assert check_espresso_machine([]) == "NO_DATA"
    assert check_espresso_machine(None) == "NO_DATA"


def test_branch_espresso_streak_reaches_two_shutdown():
    """Branch: temp > 96.0 -> True, streak >= 2 -> True."""
    cycles = [[96.5, 98.0]]
    assert check_espresso_machine(cycles) == "SHUTDOWN"


def test_branch_espresso_single_high_reading_resets():
    """Branch: temp > 96.0 -> True (streak 1, not 2), followed by <= 96.0 -> reset to 0."""
    cycles = [
        [97.0, 95.0, 96.2, 94.0],  # Isolated overheat readings that reset
        [90.0, 91.0]
    ]
    assert check_espresso_machine(cycles) == "OPTIMAL"


def test_branch_espresso_streak_not_carried_over_cycles():
    """Branch: Each cycle resets streak to 0 at the start of loop."""
    cycles = [
        [97.0],  # End cycle 1 with streak 1
        [97.0]   # Start cycle 2 resets streak to 0, so 97.0 makes streak 1, not 2
    ]
    assert check_espresso_machine(cycles) == "OPTIMAL"

