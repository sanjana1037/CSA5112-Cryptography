# -------------------------------
#   RSA Private Key Calculation
# -------------------------------

# Extended Euclidean Algorithm
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

# Modular inverse function
def mod_inverse(e, phi):
    gcd, x, y = extended_gcd(e, phi)
    if gcd != 1:
        return None  # No inverse
    return x % phi

# Given RSA values
e = 31
n = 3599

# Factorization of n = 59 × 61 (found by trial)
p = 59
q = 61

# Compute phi(n)
phi = (p - 1) * (q - 1)

# Compute private key d
d = mod_inverse(e, phi)

print("Public Key  : (e =", e, ", n =", n, ")")
print("p =", p, ", q =", q)
print("phi(n) =", phi)
print("Private Key : d =", d)
