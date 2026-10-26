# TASK 4 - Write Correct Expressions

BASE_RATE = 30.0
FAT_RATE_STEP = 0.40
SNF_RATE_STEP = 0.30
BASE_FAT = 3.5
BASE_SNF = 8.5

# Sample input values
litres = 10
fat = 4.2
snf = 8.9

# 1. Compute the number of fat and SNF steps using round() to avoid floating-point errors
fat_steps = round((fat - BASE_FAT) / 0.1, 2)
snf_steps = round((snf - BASE_SNF) / 0.1, 2)

# 2. Compute the rate per litre
rate_per_litre = BASE_RATE + (fat_steps * FAT_RATE_STEP) + (snf_steps * SNF_RATE_STEP)

# 3. Compute the total amount
total_amount = litres * rate_per_litre

print("Fat Steps:", fat_steps)
print("SNF Steps:", snf_steps)
print("Rate per Litre:", rate_per_litre)
print("Total Amount:", total_amount)

# Three expressions that demonstrate unexpected results / surprises:
print("\n--- Unexpected Results Examples ---")
print("1. (4.2 - 3.5) / 0.1 =", (4.2 - 3.5) / 0.1)  # Gives 7.000000000000001 due to binary float representation
print("2. int(-5.5) =", int(-5.5))                    # Truncates towards zero, resulting in -5 instead of flooring to -6
print("3. 2.0 <= 4.2 <= 7.0 and 5.0 =", 2.0 <= 4.2 <= 7.0 and 5.0)  # Evaluates to 5.0 due to boolean 'and' short-circuiting behavior