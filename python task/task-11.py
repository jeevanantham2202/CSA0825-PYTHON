"""
TASK 11: Final Design Recommendation & Rate Configuration
Demonstrating:
1. Exact financial calculation using Python's Decimal module.
2. Banker's rounding (ROUND_HALF_UP / ROUND_HALF_EVEN) per payment.
3. Decoupled rate revisions via external JSON configuration vs hardcoded module.
"""

from decimal import Decimal, ROUND_HALF_UP
import json
import os
import sys
import time

# --- Part 1: Rate Configuration (JSON vs Module) ---

DEFAULT_CONFIG = {
    "BASE_RATE": "30.00",
    "FAT_BASE": "3.5",
    "SNF_BASE": "8.5",
    "FAT_STEP_VALUE": "0.40",
    "SNF_STEP_VALUE": "0.30",
    "STEP_SIZE": "0.1"
}

CONFIG_FILE = "rate_card.json"

def initialize_rate_card(filepath=CONFIG_FILE):
    """Creates a default JSON configuration file if it does not exist."""
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)

def load_rates(filepath=CONFIG_FILE):
    """
    Reads rates from JSON file. Allows rate revisions in ONE place 
    without modifying or redistributing source code.
    """
    with open(filepath, "r") as f:
        data = json.load(f)
    return {k: Decimal(v) for k, v in data.items()}


# --- Part 2: Core Calculation Functions (Recommended Design) ---

def calculate_rate_per_litre(fat: Decimal, snf: Decimal, rates: dict) -> Decimal:
    """
    Calculates rate per litre using exact Decimal step arithmetic.
    Rounds step count and rate to 2 decimal places.
    """
    fat_diff = fat - rates["FAT_BASE"]
    snf_diff = snf - rates["SNF_BASE"]

    # Calculate step count: rounded to nearest integer step
    fat_steps = (fat_diff / rates["STEP_SIZE"]).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    snf_steps = (snf_diff / rates["STEP_SIZE"]).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

    rate = rates["BASE_RATE"] + (fat_steps * rates["FAT_STEP_VALUE"]) + (snf_steps * rates["SNF_STEP_VALUE"])
    return rate.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def calculate_payout(litres: Decimal, rate: Decimal) -> Decimal:
    """
    Computes payment rounded per entry to 2 decimal places (Bank Currency Standard).
    """
    amount = litres * rate
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


# --- Part 3: Alternative Analysis & Benchmarking ---

def benchmark_json_loading(filepath=CONFIG_FILE):
    """Analyzes startup time and memory overhead for reading external JSON configuration."""
    start_time = time.perf_counter()
    with open(filepath, "r") as f:
        raw_data = json.load(f)
    elapsed_time = time.perf_counter() - start_time
    
    memory_size = sys.getsizeof(raw_data)
    return elapsed_time, memory_size


# --- Execution and Demonstration ---

if __name__ == "__main__":
    initialize_rate_card()
    
    # 1. Benchmark external configuration load
    load_time, mem_size = benchmark_json_loading()
    rates = load_rates()

    print("=== TASK 11: FINAL DESIGN VERIFICATION ===")
    print(f"JSON Rate Card Loaded in: {load_time * 1e6:.2f} microseconds")
    print(f"Configuration Memory Overhead: {mem_size} bytes\n")

    # Sample farmer entries: (Farmer ID, Litres, Fat %, SNF %)
    sample_records = [
        ("F101", "10.0", "3.5", "8.5"),
        ("F102", "8.5", "4.2", "8.7"),
        ("F103", "12.0", "3.1", "8.3")
    ]

    total_payout = Decimal("0.00")

    print(f"{'ID':<6} {'Litres':<8} {'Fat%':<6} {'SNF%':<6} {'Rate(Rs)':<10} {'Payout(Rs)':<10}")
    print("-" * 50)

    for farmer_id, lit_str, fat_str, snf_str in sample_records:
        litres = Decimal(lit_str)
        fat = Decimal(fat_str)
        snf = Decimal(snf_str)

        rate = calculate_rate_per_litre(fat, snf, rates)
        payout = calculate_payout(litres, rate)
        total_payout += payout

        print(f"{farmer_id:<6} {lit_str:<8} {fat_str:<6} {snf_str:<6} {rate:<10} {payout:<10}")

    print("-" * 50)
    print(f"Total Ten-Day Cooperative Payout: Rs {total_payout}")