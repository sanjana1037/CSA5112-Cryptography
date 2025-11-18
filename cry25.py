import math

# RSA public values (example)
n = 3599          # n = p*q
e = 31            # public exponent

# Suppose someone tells us this plaintext block was used:
M = 59            # plaintext block that shares a factor with n

# Step 1: Compute gcd(M, n)
g = math.gcd(M, n)

print("GCD(M, n) =", g)

# If gcd > 1, we discovered a prime factor of n
if g > 1:
    p = g
    q = n // p
    print("Factor found! p =", p, ", q =", q)

    # Compute phi(n)
    phi = (p - 1) * (q - 1)

    # Extended Euclid for modular inverse
    def egcd(a, b):
        if b == 0:
            return a, 1, 0
        gcd, x1, y1 = egcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y

    def mod_inverse(a, m):
        gcd, x, y = egcd(a, m)
        if gcd != 1:
            return None
        return x % m

    # Compute private key d
    d = mod_inverse(e, phi)
    print("Private Key d =", d)
else:
    print("No factor discovered.")
