import math

def factorial_log2(n):
    """Compute log2(n!) approximately."""
    return sum(math.log2(i) for i in range(1, n+1))

# Total possible keys ignoring duplicates
total_letters = 25  # I/J combined
log2_total_keys = factorial_log2(total_letters)
print(f"Approximate total possible keys (ignoring duplicates): 2^{log2_total_keys:.2f}")

# Effectively unique keys
# Adjust for row and column permutations: 5!^5
row_col_factor = math.factorial(5) ** 5
log2_effective_keys = log2_total_keys - math.log2(row_col_factor)
print(f"Approximate effectively unique keys: 2^{log2_effective_keys:.2f}")
