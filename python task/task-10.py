"""
TASK 10: Compare Expectations with Execution
Bloom's Level: K4 - Analyse

Requirements:
- Compare float vs Decimal totals for 300, 6,000, and 150,000 payments.
- Measure execution time using time.perf_counter().
- Compare rounding each payment vs rounding only the total.
- Alternative Concept: Recalculation vs Precomputed Rate Table (Dictionary O(1) lookup).
"""

import sys
import time
from decimal import Decimal, ROUND_HALF_UP

# Rate Constants
BASE_RATE = 30.00
FAT_STEP = 0.40
SNF_STEP = 0.30

# Decimal Constants
DEC_BASE = Decimal("30.00")
DEC_FAT_STEP = Decimal("0.40")
DEC_SNF_STEP = Decimal("0.30")


# --- 1. Float Calculation Functions ---
def calc_rate_float(fat, snf):
    fat_steps = round((fat - 3.5) * 10)
    snf_steps = round((snf - 8.5) * 10)
    return round(BASE_RATE + (fat_steps * FAT_STEP) + (snf_steps * SNF_STEP), 2)


def process_float(dataset, round_each=True):
    total = 0.0
    for litres, fat, snf in dataset:
        rate = calc_rate_float(fat, snf)
        if round_each:
            total += round(litres * rate, 2)
        else:
            total += litres * rate
    return round(total, 2)


# --- 2. Decimal Calculation Functions ---
def calc_rate_decimal(fat_str, snf_str):
    fat_steps = (Decimal(fat_str) - Decimal("3.5")) / Decimal("0.1")
    snf_steps = (Decimal(snf_str) - Decimal("8.5")) / Decimal("0.1")
    rate = DEC_BASE + (fat_steps * DEC_FAT_STEP) + (snf_steps * DEC_SNF_STEP)
    return rate.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def process_decimal(dataset_str, round_each=True):
    total = Decimal("0.00")
    for litres_str, fat_str, snf_str in dataset_str:
        rate = calc_rate_decimal(fat_str, snf_str)
        if round_each:
            total += (Decimal(litres_str) * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        else:
            total += Decimal(litres_str) * rate
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


# --- 3. Precomputed Dictionary Rate Table (Alternative Concept) ---
def build_rate_table():
    """Precomputes rates for all valid 0.1 increments:
    Fat: 2.0 to 7.0 (51 steps), SNF: 6.0 to 10.0 (41 steps) -> 2,091 total pairs.
    """
    table = {}
    for f in range(20, 71):
        fat = f / 10.0
        for s in range(60, 101):
            snf = s / 10.0
            table[(round(fat, 1), round(snf, 1))] = calc_rate_float(fat, snf)
    return table


def process_with_lookup(dataset, rate_table):
    total = 0.0
    for litres, fat, snf in dataset:
        rate = rate_table[(fat, snf)]
        total += round(litres * rate, 2)
    return round(total, 2)


# --- Benchmark Runner ---
def run_benchmarks():
    # Base batch of typical cooperative entries
    base_entries = [
        (10.0, 3.5, 8.5),
        (8.5, 4.2, 8.7),
        (12.0, 3.1, 8.3),
        (15.0, 3.8, 8.6),
        (7.0, 4.0, 8.9),
        (11.5, 3.3, 8.4)
    ]
    base_entries_str = [(str(l), str(f), str(s)) for l, f, s in base_entries]

    sizes = [300, 6000, 150000]

    print("=" * 88)
    print("TASK 10: EXPERIMENTAL BENCHMARK REPORT (FLOAT vs DECIMAL)")
    print("=" * 88)
    print(f"{'Count (n)':<10} | {'Type':<9} | {'Total (Rs)':<16} | {'Diff vs Dec':<14} | {'Time (sec)':<12}")
    print("-" * 88)

    for n in sizes:
        multiplier = n // len(base_entries)
        dataset_float = base_entries * multiplier
        dataset_str = base_entries_str * multiplier

        # Benchmark Float (rounding each payment)
        t0 = time.perf_counter()
        tot_float = process_float(dataset_float, round_each=True)
        t_float = time.perf_counter() - t0

        # Benchmark Decimal (exact banking standard)
        t0 = time.perf_counter()
        tot_dec = process_decimal(dataset_str, round_each=True)
        t_dec = time.perf_counter() - t0

        diff = abs(float(tot_dec) - tot_float)

        print(f"{n:<10} | {'Float':<9} | {tot_float:<16.2f} | Rs {diff:<11.2f} | {t_float:<12.5f}")
        print(f"{n:<10} | {'Decimal':<9} | {str(tot_dec):<16} | {'0.00 (Base)':<14} | {t_dec:<12.5f}")
        print("-" * 88)

    # --- Rounding Comparison ---
    print("\n" + "=" * 88)
    print("ROUNDING COMPARISON: Rounding Each Payment vs Rounding Only Grand Total")
    print("=" * 88)
    n_sample = 6000
    dataset_6k = base_entries * (n_sample // len(base_entries))

    tot_each = process_float(dataset_6k, round_each=True)
    tot_end = process_float(dataset_6k, round_each=False)
    diff_rounding = abs(tot_each - tot_end)

    print(f"Sample Size: {n_sample} entries")
    print(f"Total when rounding EACH payment : Rs {tot_each:.2f}")
    print(f"Total when rounding ONLY at end  : Rs {tot_end:.2f}")
    print(f"Discrepancy caused by drift      : Rs {diff_rounding:.2f}")
    print("Note: In bank settlements, each individual payout voucher is rounded to 2 decimals.")

    # --- Alternative Concept Analysis ---
    print("\n" + "=" * 88)
    print("ALTERNATIVE CONCEPT: Dynamic Recalculation vs Precomputed Rate Table (O(1) Lookup)")
    print("=" * 88)
    rate_table = build_rate_table()
    table_size = sys.getsizeof(rate_table)
    pair_count = len(rate_table)

    test_data = base_entries * (150000 // len(base_entries))

    # Time recalculation
    t0 = time.perf_counter()
    _ = process_float(test_data, round_each=True)
    t_recalc = time.perf_counter() - t0

    # Time lookup
    t0 = time.perf_counter()
    _ = process_with_lookup(test_data, rate_table)
    t_lookup = time.perf_counter() - t0

    speedup = t_recalc / t_lookup if t_lookup > 0 else 0

    print(f"Entries processed      : 150,000")
    print(f"Unique (fat, snf) pairs: {pair_count} combinations stored")
    print(f"Memory for dictionary  : {table_size} bytes (~{table_size / 1024:.2f} KB)")
    print(f"Recalculation Time     : {t_recalc:.4f} seconds")
    print(f"Table Lookup Time      : {t_lookup:.4f} seconds")
    print(f"Lookup Speedup         : {speedup:.2f}x faster")
    print("=" * 88)


if __name__ == "__main__":
    run_benchmarks()