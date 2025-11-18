# -------------------------------------------------------
# Demonstration: Why Bob cannot reuse the same modulus n
# -------------------------------------------------------

# Example RSA values (Bob leaked d)
e = 31
d = 3031
n = 3599    # modulus used in RSA (should be kept secret if d is leaked)

# Step 1: Compute k = e*d − 1 = multiple of phi(n)
k = e * d - 1
print("k = ed - 1 =", k)

# Step 2: Find any factor of k by trial (we look for m such that phi(n) = k/m)
# This simulates an attacker finding φ(n)
factors = []
for i in range(2, 5000):
    if k % i == 0:
        factors.append(i)

print("Small factors of k (attacker tries these):", factors[:10])

# Step 3: Try to solve for p and q using φ(n)
# phi(n) = (p-1)(q-1) = pq - (p+q) + 1 = n - (p+q) + 1
# => p + q = n - phi(n) + 1

for m in factors:
    phi = k // m
    # Find p and q using quadratic formula:
    # x^2 - Sx + n = 0   where S = p + q
    S = n - phi + 1
    discriminant = S*S - 4*n

    if discriminant >= 0:
        sqrt_disc = int(discriminant**0.5)
        if sqrt_disc * sqrt_disc == discriminant:
            p = (S + sqrt_disc) // 2
            q = (S - sqrt_disc) // 2
            if p*q == n:
                print("\nRSA BROKEN!")
                print("Recovered p =", p)
                print("Recovered q =", q)
                break
