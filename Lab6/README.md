# Lab 6: Code and Branch Coverage Analysis

## 1. Objective

The objective of this laboratory exercise is to systematically analyze and elevate the test coverage of the coffee shop order processing system using Python, `pytest`, and `coverage.py`. The assignment targets:
- At least **90% Line (Statement) Coverage**.
- At least **90% Branch Coverage**.

---

## 2. Application Description

The target application module is [`coffee_shop_order.py`](coffee_shop_order.py), consisting of two primary functions:
1. **`process_order_batch(orders, tax_rate)`**:
   - Validates input format (orders as `list`, non-negative `tax_rate`).
   - Iterates through orders, filtering out unpaid transactions (`paid == False`).
   - Prices items by size: `small` (\$3.00), `medium` (\$4.50, default), `large` (\$6.00). Invalid sizes increment rejection count.
   - Evaluates modifier list (`customizations`):
     - Negative modifier costs increment `rejected_items`.
     - `allergen_alert` triggers rejection increment; if `strict_allergy` is enabled, resets `item_total` to 0.0 and aborts item calculation.
     - `syrup` modifier charges are capped at \$1.50 max.
     - Standard modifiers are added directly.
   - Applies a 10% membership discount (`is_member == True`).
   - Computes tax-inclusive total.
   - Determines batch status:
     - `AUDIT_REJECTED` if `rejected_items > 4`.
     - `NO_SALE` if `batch_total == 0.0`.
     - `COMPLETED` otherwise.
2. **`check_espresso_machine(temperature_cycles)`**:
   - Returns `"NO_DATA"` if input cycles are empty or None.
   - Tracks consecutive temperature readings above 96.0°C within each cycle.
   - Returns `"SHUTDOWN"` if 2 consecutive readings exceed 96.0°C.
   - Resets streak to 0 whenever temperature drops to 96.0°C or below.
   - Returns `"OPTIMAL"` if no cycle trips shutdown.

---

## 3. Difference Between Code and Branch Coverage

- **Code (Line / Statement) Coverage**: Measures the proportion of executable statements (lines) executed during testing. A suite with 100% line coverage confirms that every line ran at least once, but it does not guarantee that every decision outcome (both `True` and `False` edges) of conditional logic was exercised.
- **Branch Coverage**: Evaluates every control flow decision point (e.g. `if`, `elif`, `else`, `while`, `for`) to ensure both `True` and `False` branches are taken. Branch coverage detects edge cases where conditional logic may skip code or take default fallbacks unintentionally.

---

## 4. Initial Coverage Results

Running the starter test file [`test_coffee_shop.py`](test_coffee_shop.py):

### Initial Line Coverage
- Command:
  ```bash
  coverage run -m pytest
  coverage report -m
  ```
- **Line Coverage**: **48%** on `coffee_shop_order.py` (26 of 54 statements executed, 28 missed: lines 3, 10, 14, 17-21, 31-32, 35-38, 40, 45, 52, 54, 59-71).
- Total coverage: 54%.

### Initial Branch Coverage
- Command:
  ```bash
  coverage run --branch -m pytest
  coverage report -m
  ```
- **Branch Coverage**: **43%** on `coffee_shop_order.py` (38 branches, 10 partial branches, 28 missing statements). Total coverage: 47%.

---

## 5. Test Cases Implemented

### Suite A: Code Coverage Suite (`CodeCoverageTest_coffee_shop_order.py`)
18 distinct unit tests exercising every execution statement:
1. `test_invalid_orders_type`: Validates `ValueError` for non-list inputs.
2. `test_invalid_negative_tax_rate`: Validates `ValueError` for negative tax rate.
3. `test_empty_orders_no_sale`: Validates `NO_SALE` return on empty batch.
4. `test_unpaid_order_skipped`: Ensures unpaid orders are bypassed.
5. `test_size_small`: Confirms \$3.00 base pricing.
6. `test_size_medium_default`: Confirms \$4.50 default pricing.
7. `test_size_large`: Confirms \$6.00 base pricing.
8. `test_unknown_size_rejected`: Checks handling and rejection count for invalid sizes.
9. `test_customization_negative_cost`: Verifies negative customization costs are discarded.
10. `test_customization_allergen_alert_strict`: Validates strict allergy zeroing and early loop exit.
11. `test_customization_allergen_alert_non_strict`: Confirms non-strict allergy retains base total.
12. `test_customization_syrup_cap`: Exercises both below and above \$1.50 syrup cost threshold.
13. `test_customization_standard_addon`: Tests standard positive add-on modifier costs.
14. `test_member_discount`: Validates 10% membership discount calculation.
15. `test_audit_rejected_status`: Tests audit status when rejected items exceed 4.
16. `test_espresso_no_data`: Validates `NO_DATA` when cycles are empty or None.
17. `test_espresso_shutdown`: Verifies `SHUTDOWN` triggered on 2 consecutive readings > 96.0°C.
18. `test_espresso_streak_resets_optimal`: Verifies overheat streak resets upon safe temperature readings.

### Suite B: Branch Coverage Suite (`BranchCoverageTest_coffee_shop_order.py`)
15 independent tests targeting decision branch paths:
1. `test_branch_input_validation_non_list`: Tests non-list validation branch (`True`).
2. `test_branch_input_validation_negative_tax`: Tests negative tax branch (`False` on list, `True` on tax).
3. `test_branch_empty_order_list_no_sale`: Tests loop zero-iteration branch.
4. `test_branch_order_unpaid_vs_paid`: Tests both `True` and `False` paths for `not order.get("paid")`.
5. `test_branch_size_evaluation_all_paths`: Tests all four branches of size conditional ladder (`small`, `medium`, `large`, `else`).
6. `test_branch_customization_cost_negative_vs_positive`: Tests negative cost branch vs positive cost branch.
7. `test_branch_allergen_alert_strict_true`: Tests allergen alert with `strict_allergy == True`.
8. `test_branch_allergen_alert_strict_false`: Tests allergen alert with `strict_allergy == False`.
9. `test_branch_syrup_cost_boundary`: Tests syrup ternary condition (`cost <= 1.5` vs `cost > 1.5`).
10. `test_branch_member_discount_branching`: Tests member discount branch taken vs bypassed.
11. `test_branch_audit_rejected_threshold`: Tests exact boundary condition for `rejected_items > 4` (both > 4 and == 4).
12. `test_branch_espresso_falsy_cycles`: Tests `not temperature_cycles` truthiness branches (empty list and None).
13. `test_branch_espresso_streak_reaches_two_shutdown`: Tests temperature streak tripping shutdown.
14. `test_branch_espresso_single_high_reading_resets`: Tests `else` reset branch when reading <= 96.0°C.
15. `test_branch_espresso_streak_not_carried_over_cycles`: Confirms per-cycle streak re-initialization.

---

## 6. Final Code Coverage Results

- Command:
  ```bash
  coverage run -m pytest CodeCoverageTest_coffee_shop_order.py
  coverage report -m
  ```
- **Line Coverage**: **100%** on `coffee_shop_order.py` (54/54 statements, 0 missing).

---

## 7. Final Branch Coverage Results

- Command:
  ```bash
  coverage run --branch -m pytest BranchCoverageTest_coffee_shop_order.py
  coverage report -m
  ```
- **Branch Coverage**: **100%** on `coffee_shop_order.py` (54 statements, 38 branches, 0 partial, 0 missed).

---

## 8. Commands Used

```bash
# Navigate to Lab 6 directory
cd Lab6

# Run initial coverage
coverage run -m pytest
coverage report -m
coverage run --branch -m pytest
coverage report -m

# Run Code Coverage Test Suite
coverage run -m pytest CodeCoverageTest_coffee_shop_order.py
coverage report -m

# Run Branch Coverage Test Suite
coverage run --branch -m pytest BranchCoverageTest_coffee_shop_order.py
coverage report -m
```

---

## 9. Screenshot References

- `screenshots/01_initial_coverage.png`: Terminal output for starter coverage run showing 48% line and 43% branch coverage.
- `screenshots/02_final_code_coverage.png`: Terminal output for code coverage suite showing 100% statement coverage.
- `screenshots/03_final_branch_coverage.png`: Terminal output for branch coverage suite showing 100% branch coverage.

---

## 10. Conclusion

By designing targeted unit and branch test suites, coverage on `coffee_shop_order.py` improved from an initial 48% line / 43% branch coverage to **100% line coverage** and **100% branch coverage**, comfortably surpassing the 90% threshold requirement.
