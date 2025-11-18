import numpy as np

# -----------------------------
# Modular inverse (for numbers)
# -----------------------------
def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("No modular inverse exists")

# -----------------------------
# Modular matrix inverse (2×2)
# -----------------------------
def matrix_mod_inverse(matrix, mod):
    det = int(np.round(np.linalg.det(matrix))) % mod
    det_inv = mod_inverse(det, mod)

    # adjugate for 2×2
    adj = np.array([[matrix[1,1], -matrix[0,1]],
                    [-matrix[1,0], matrix[0,0]]])

    inv = (det_inv * adj) % mod
    return inv

# -----------------------------
# Main Known-Plaintext Attack
# -----------------------------
print("Enter 4 numbers for plaintext matrix P (two 2-letter blocks):")
P = np.zeros((2,2), dtype=int)
P[0,0], P[0,1], P[1,0], P[1,1] = map(int, input().split())

print("Enter 4 numbers for ciphertext matrix C (matching blocks):")
C = np.zeros((2,2), dtype=int)
C[0,0], C[0,1], C[1,0], C[1,1] = map(int, input().split())

# Compute inverse of plaintext matrix
try:
    P_inv = matrix_mod_inverse(P, 26)
except:
    print("Plaintext matrix is NOT invertible modulo 26 — cannot solve.")
    exit()

print("\nInverse of plaintext matrix P⁻¹ (mod 26):")
print(P_inv)

# Recover key: K = C × P⁻¹ (mod 26)
K = (C.dot(P_inv)) % 26

print("\nRecovered Hill Cipher Key Matrix K (mod 26):")
print(K)
