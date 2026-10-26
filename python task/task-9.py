"""
TASK 9: Implement and Test the Calculator
Bloom's Level: K3 - Apply

Tests:
1. Normal entries (above and below standard)
2. Boundary entries (standard, lowest allowed fat/SNF, highest allowed fat/SNF)
3. Invalid entries (text, negative quantity, out-of-range fat/SNF)
4. Hand-calculated 5-entry batch test
"""

# Rate Card Constants
BASE_RATE = 30.00
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30

# Allowed Quality Limits
FAT_MIN, FAT_MAX = 2.0, 7.0
SNF_MIN, SNF_MAX = 6.0, 10.0


def validate_entry(litres, fat, snf):
    """Validates inputs for numeric type, positive volume, and valid quality ranges.
    Returns: (is_valid: bool, error_message: str)
    """
    try:
        litres = float(litres)
        fat = float(fat)
        snf = float(snf)
    except (ValueError, TypeError):
        return False, "Inputs must be numeric."

    if litres < 0:
        return False, "Quantity cannot be negative."
    if not (FAT_MIN <= fat <= FAT_MAX):
        return False, f"Fat % must be between {FAT_MIN} and {FAT_MAX}."
    if not (SNF_MIN <= snf <= SNF_MAX):
        return False, f"SNF % must be between {SNF_MIN} and {SNF_MAX}."

    return True, "Valid"


def rate_per_litre(fat, snf):
    """Computes price per litre using integer steps to avoid binary floating-point drift."""
    # Scale by 10 to ensure exact whole steps
    fat_steps = round((fat - 3.5) * 10)
    snf_steps = round((snf - 8.5) * 10)

    rate = BASE_RATE + (fat_steps * FAT_STEP_VALUE) + (snf_steps * SNF_STEP_VALUE)
    return round(rate, 2)


def payout(litres, fat, snf):
    """Computes payment for a single valid entry."""
    is_valid, msg = validate_entry(litres, fat, snf)
    if not is_valid:
        raise ValueError(msg)
    return round(float(litres) * rate_per_litre(float(fat), float(snf)), 2)


def run_tests():
    print("=" * 75)
    print("TASK 9: AUTOMATED TEST SUITE & EVIDENCE TABLE")
    print("=" * 75)
    print(f"{'Category':<15} | {'Input (L, Fat, SNF)':<20} | {'Expected':<12} | {'Actual':<12} | {'Status'}")
    print("-" * 75)

    # 1. Normal entries
    # 4.2 fat (+7 steps = +2.80), 8.7 snf (+2 steps = +0.60) -> 30 + 3.40 = 33.40
    r1 = rate_per_litre(4.2, 8.7)
    assert r1 == 33.40, f"Expected 33.40, got {r1}"
    print(f"{'Normal':<15} | {'(10, 4.2, 8.7)':<20} | {'33.40':<12} | {r1:<12.2f} | PASS")

    # 3.1 fat (-4 steps = -1.60), 8.3 snf (-2 steps = -0.60) -> 30 - 2.20 = 27.80
    r2 = rate_per_litre(3.1, 8.3)
    assert r2 == 27.80, f"Expected 27.80, got {r2}"
    print(f"{'Normal':<15} | {'(10, 3.1, 8.3)':<20} | {'27.80':<12} | {r2:<12.2f} | PASS")

    # 2. Boundary entries
    # Standard: 3.5 fat, 8.5 snf -> 30.00
    r_std = rate_per_litre(3.5, 8.5)
    assert r_std == 30.00, f"Expected 30.00, got {r_std}"
    print(f"{'Boundary (Std)':<15} | {'(10, 3.5, 8.5)':<20} | {'30.00':<12} | {r_std:<12.2f} | PASS")

    # Lowest: 2.0 fat (-15 steps = -6.00), 6.0 snf (-25 steps = -7.50) -> 30 - 13.50 = 16.50
    # (Note: Lowest allowed values 2.0 and 6.0 give 16.50)
    r_low = rate_per_litre(2.0, 6.0)
    assert r_low == 16.50, f"Expected 16.50, got {r_low}"
    print(f"{'Boundary (Min)':<15} | {'(10, 2.0, 6.0)':<20} | {'16.50':<12} | {r_low:<12.2f} | PASS")

    # Highest: 7.0 fat (+35 steps = +14.00), 10.0 snf (+15 steps = +4.50) -> 30 + 18.50 = 48.50
    r_high = rate_per_litre(7.0, 10.0)
    assert r_high == 48.50, f"Expected 48.50, got {r_high}"
    print(f"{'Boundary (Max)':<15} | {'(10, 7.0, 10.0)':<20} | {'48.50':<12} | {r_high:<12.2f} | PASS")

    # 3. Invalid entries
    v_text, _ = validate_entry("ten", 3.5, 8.5)
    assert not v_text, "Failed to reject text"
    print(f"{'Invalid (Text)':<15} | {'(\"ten\", 3.5, 8.5)':<20} | {'Rejected':<12} | {'Rejected':<12} | PASS")

    v_neg, _ = validate_entry(-5.0, 3.5, 8.5)
    assert not v_neg, "Failed to reject negative litres"
    print(f"{'Invalid (Qty)':<15} | {'(-5.0, 3.5, 8.5)':<20} | {'Rejected':<12} | {'Rejected':<12} | PASS")

    v_fat, _ = validate_entry(10.0, 1.5, 8.5)
    assert not v_fat, "Failed to reject out-of-bounds fat"
    print(f"{'Invalid (Fat)':<15} | {'(10.0, 1.5, 8.5)':<20} | {'Rejected':<12} | {'Rejected':<12} | PASS")

    # 4. Hand-calculated set of 5 entries
    hand_entries = [
        (10.0, 3.5, 8.5),  # Rate: 30.00 -> Pay: 300.00
        (8.5,  4.2, 8.7),  # Rate: 33.40 -> Pay: 283.90
        (12.0, 3.1, 8.3),  # Rate: 27.80 -> Pay: 333.60
        (15.0, 3.5, 8.5),  # Rate: 30.00 -> Pay: 450.00
        (20.0, 4.0, 9.0),  # Rate: 33.50 -> Pay: 670.00
    ]
    # Hand Total = 300.00 + 283.90 + 333.60 + 450.00 + 670.00 = 2037.50
    hand_total = sum(payout(l, f, s) for l, f, s in hand_entries)
    expected_hand_total = 2037.50

    assert round(hand_total, 2) == expected_hand_total, f"Expected {expected_hand_total}, got {hand_total}"
    print(f"{'Hand Batch (5)':<15} | {'5 Entries':<20} | {expected_hand_total:<12.2f} | {hand_total:<12.2f} | PASS")
    print("-" * 75)
    print("ALL TESTS PASSED SUCCESSFULLY! ZERO ERRORS.")


if __name__ == "__main__":
    run_tests()