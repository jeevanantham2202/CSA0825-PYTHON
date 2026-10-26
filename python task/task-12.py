"""
TASK 12: Day-4 Design Challenge - Re-evaluate and Adapt the Design
Features:
- Handles 2-decimal automated milk analyser readings (e.g., 4.25% Fat, 8.65% SNF).
- Dynamic Rate Card selection based on season (April-June vs Standard).
- Volume-based bonus (Rs 0.50/L for > 500 Litres in a 10-day period).
- Exact arithmetic and currency rounding using Python's Decimal module.
"""

from decimal import Decimal, ROUND_HALF_UP

# --- Rate Configuration Constants ---
RATE_CARDS = {
    "STANDARD": {
        "BASE_RATE": Decimal("30.00"),
        "FAT_BASE": Decimal("3.5"),
        "SNF_BASE": Decimal("8.5"),
        "FAT_STEP_VALUE": Decimal("0.40"),
        "SNF_STEP_VALUE": Decimal("0.30"),
        "STEP_SIZE": Decimal("0.1")
    },
    "SUMMER": {  # April to June seasonal revision
        "BASE_RATE": Decimal("32.00"),
        "FAT_BASE": Decimal("3.5"),
        "SNF_BASE": Decimal("8.5"),
        "FAT_STEP_VALUE": Decimal("0.45"),
        "SNF_STEP_VALUE": Decimal("0.30"),
        "STEP_SIZE": Decimal("0.1")
    }
}

BONUS_THRESHOLD_LITRES = Decimal("500.00")
BONUS_RATE_PER_LITRE = Decimal("0.50")


def get_rate_card(month: int) -> dict:
    """Returns the applicable rate card based on the month (1-12)."""
    if 4 <= month <= 6:
        return RATE_CARDS["SUMMER"]
    return RATE_CARDS["STANDARD"]


def calculate_rate_per_litre(fat: Decimal, snf: Decimal, rates: dict) -> Decimal:
    """
    Computes rate per litre handling 2-decimal inputs with ROUND_HALF_UP.
    Steps are calculated relative to 0.1% standard step sizes.
    """
    fat_diff = fat - rates["FAT_BASE"]
    snf_diff = snf - rates["SNF_BASE"]

    # When analyser provides 2 decimals, step count can be fractional.
    # We maintain fractional steps or round to 2 decimal places:
    fat_steps = fat_diff / rates["STEP_SIZE"]
    snf_steps = snf_diff / rates["STEP_SIZE"]

    rate = rates["BASE_RATE"] + (fat_steps * rates["FAT_STEP_VALUE"]) + (snf_steps * rates["SNF_STEP_VALUE"])
    return rate.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_entry_payout(litres: Decimal, rate: Decimal) -> Decimal:
    """Calculates payout per shift entry, rounded to nearest 2 decimal places."""
    amount = litres * rate
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_volume_bonus(total_litres: Decimal) -> Decimal:
    """Computes bonus if 10-day supply exceeds 500 Litres."""
    if total_litres > BONUS_THRESHOLD_LITRES:
        bonus = total_litres * BONUS_RATE_PER_LITRE
        return bonus.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return Decimal("0.00")


def process_ten_day_statement(farmer_id: str, entries: list, month: int):
    """
    Processes all 10-day entries for a farmer, applying seasonal rates and volume bonus.
    entries: List of tuples -> (litres_str, fat_str, snf_str)
    """
    rates = get_rate_card(month)
    season_name = "Summer (Apr-Jun)" if 4 <= month <= 6 else "Standard"

    print(f"\n=======================================================")
    print(f"Farmer ID: {farmer_id} | Season: {season_name} (Month: {month})")
    print(f"{'Shift':<6} {'Litres':<8} {'Fat%':<8} {'SNF%':<8} {'Rate(Rs)':<10} {'Amount(Rs)':<10}")
    print("-" * 55)

    total_litres = Decimal("0.00")
    base_payout = Decimal("0.00")

    for idx, (lit_str, fat_str, snf_str) in enumerate(entries, start=1):
        litres = Decimal(lit_str)
        fat = Decimal(fat_str)
        snf = Decimal(snf_str)

        rate = calculate_rate_per_litre(fat, snf, rates)
        amount = calculate_entry_payout(litres, rate)

        total_litres += litres
        base_payout += amount

        print(f"{idx:<6} {lit_str:<8} {fat_str:<8} {snf_str:<8} {rate:<10} {amount:<10}")

    bonus = calculate_volume_bonus(total_litres)
    final_total = base_payout + bonus

    print("-" * 55)
    print(f"Total Litres Supplied : {total_litres} L")
    print(f"Base Milk Payout      : Rs {base_payout}")
    print(f"Volume Bonus (>500L)  : Rs {bonus}")
    print(f"Total Amount Payable  : Rs {final_total}")
    print(f"=======================================================")


# --- Test Cases & Demonstration ---
if __name__ == "__main__":
    # Test 1: Normal Season (January - Month 1) with high volume (>500L gets bonus)
    # Using 2-decimal analyzer readings like 4.25% Fat, 8.65% SNF
    farmer_1_entries = [
        ("60.00", "4.25", "8.65"),
        ("55.50", "3.85", "8.50"),
        ("58.00", "4.10", "8.75"),
        ("62.50", "3.60", "8.45"),
        ("59.00", "4.00", "8.60"),
        ("57.50", "4.30", "8.70"),
        ("61.00", "3.75", "8.55"),
        ("56.00", "4.15", "8.65"),
        ("58.50", "3.90", "8.50"),
        ("60.00", "4.20", "8.60")
    ]  # Total: 588.00 L (> 500 L)
    process_ten_day_statement("F201", farmer_1_entries, month=1)

    # Test 2: Summer Season (May - Month 5) with regular volume (<500L no bonus)
    farmer_2_entries = [
        ("40.00", "3.55", "8.55"),
        ("42.00", "3.75", "8.60"),
        ("38.50", "3.45", "8.40"),
        ("41.00", "3.65", "8.50"),
        ("39.00", "3.50", "8.50")
    ]  # Total: 200.50 L (<= 500 L)
    process_ten_day_statement("F202", farmer_2_entries, month=5)