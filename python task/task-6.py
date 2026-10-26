"""Milk Co-operative Payout System using Functions."""

BASE_RATE = 30.00          # Rs per litre for milk with 3.5% fat and 8.5% SNF
FAT_STEP_VALUE = 0.40      # Rs per litre for every 0.1% of fat above or below 3.5
SNF_STEP_VALUE = 0.30      # Rs per litre for every 0.1% of SNF above or below 8.5

def rate_per_litre(fat, snf):
    """Returns the price per litre, rounded to 2 decimals, based on fat and SNF."""
    fat_steps = round((fat - 3.5) / 0.1)
    snf_steps = round((snf - 8.5) / 0.1)
    rate = BASE_RATE + (fat_steps * FAT_STEP_VALUE) + (snf_steps * SNF_STEP_VALUE)
    return round(rate, 2)

def payout(litres, fat, snf):
    """Returns the amount payable to the farmer, rounded to 2 decimals."""
    rate = rate_per_litre(fat, snf)
    amount = litres * rate
    return round(amount, 2)

def ten_day_total(entries):
    """Computes the total payout for a list of daily entries (litres, fat, snf)."""
    total = 0.0
    for litres, fat, snf in entries:
        total += payout(litres, fat, snf)
    return round(total, 2)

# --- Example Testing ---
if __name__ == "__main__":
    # Sample 10-day entries for a farmer: [(litres, fat, snf), ...]
    farmer_entries = [
        (10.0, 3.5, 8.5),
        (8.5, 4.2, 8.7),
        (12.0, 3.1, 8.3)
    ]
    
    print("Ten-Day Total Payout:", ten_day_total(farmer_entries))