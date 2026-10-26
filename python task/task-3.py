# TASK 3 - Choose Variables and Name the Constants
# Define the rates and limits as named constants so that a rate revision is made in one place only

BASE_RATE = 30.0
FAT_RATE_STEP = 0.40
SNF_RATE_STEP = 0.30
MAX_LITRES_LIMIT = 500

def calculate_payment(litres, fat, snf):
    # Using the named constants in calculations
    rate_per_litre = BASE_RATE + (fat * FAT_RATE_STEP) + (snf * SNF_RATE_STEP)
    return litres * rate_per_litre

# Example test
print("Calculated Payment:", calculate_payment(10, 3.5, 8.5))