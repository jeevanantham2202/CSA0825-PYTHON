"""Task 8: Algorithmic problem-solving and implementation for 
calculating a farmer's ten-day total milk payment.
"""

# Constants for milk rate calculation
BASE_RATE = 30.00
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30

def validate_entry(litres, fat, snf):
    """Validates input ranges to ensure logical correctness."""
    if litres < 0:
        return False, "Error: Quantity in litres cannot be negative."
    if not (2.0 <= fat <= 7.0):
        return False, "Error: Fat percentage must be between 2.0% and 7.0%."
    if not (6.0 <= snf <= 10.0):
        return False, "Error: SNF percentage must be between 6.0% and 10.0%."
    return True, "Valid"

def compute_payment(litres, fat, snf):
    """Computes the rate per litre and total payout for a single shift/entry."""
    fat_steps = round((fat - 3.5) / 0.1, 2)
    snf_steps = round((snf - 8.5) / 0.1, 2)
    
    rate = round(BASE_RATE + (fat_steps * FAT_STEP_VALUE) + (snf_steps * SNF_STEP_VALUE), 2)
    payout = round(litres * rate, 2)
    return rate, payout

def calculate_ten_day_total(entries):
    """Calculates the cumulative ten-day total using a running sum (O(1) space complexity).
    
    entries: List of tuples in the format (litres, fat, snf)
    """
    total_litres = 0.0
    total_amount = 0.0
    
    print(f"{'Shift':<6} | {'Litres':<8} | {'Fat%':<6} | {'SNF%':<6} | {'Rate (Rs)':<10} | {'Amount (Rs)':<12}")
    print("-" * 60)
    
    for i, entry in enumerate(entries, start=1):
        litres, fat, snf = entry
        
        # Step 1: Validate
        is_valid, message = validate_entry(litres, fat, snf)
        if not is_valid:
            print(f"Entry {i}: {message}")
            continue
            
        # Step 2: Compute
        rate, payout = compute_payment(litres, fat, snf)
        
        # Step 3: Accumulate running totals
        total_litres += litres
        total_amount += payout
        
        print(f"Day {i:<2} | {litres:<8.1f} | {fat:<6.1f} | {snf:<6.1f} | {rate:<10.2f} | {payout:<12.2f}")
        
    print("-" * 60)
    return round(total_litres, 2), round(total_amount, 2)

if __name__ == "__main__":
    # Sample 3-entry test dataset (simulating a portion of the 10-day entries)
    sample_entries = [
        (10.0, 3.5, 8.5),
        (8.5, 4.2, 8.7),
        (12.0, 3.1, 8.3)
    ]
    
    total_qty, total_val = calculate_ten_day_total(sample_entries)
    print(f"\nTotal Litres Supplied : {total_qty} L")
    print(f"Total Ten-Day Payout  : Rs {total_val}")