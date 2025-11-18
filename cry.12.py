import numpy as np

# -----------------------------
# Utility Functions
# -----------------------------

def char_to_num(c):
    return ord(c) - ord('a')

def num_to_char(n):
    return chr(n + ord('a'))

def mod_inverse(a, m):
    """Return modular inverse of a under mod m."""
    for x in range(1, m):
        if (a * x) % m == 0:
            continue
        if (a * x) % m == 1:
            return x
    raise ValueError("Modular inverse does not exist")

# -----------------------------
# Hill Cipher Encryption
# -----------------------------

def hill_encrypt(plaintext, key):
    plaintext = plaintext.replace(" ", "").lower()
    if len(plaintext) % 2 != 0:
        plaintext += 'x'   # padding

    # Convert to numbers
    pairs = []
    for i in range(0, len(plaintext), 2):
        a = char_to_num(plaintext[i])
        b = char_to_num(plaintext[i+1])
        pairs.append([a, b])

    print("\n--- Encryption Calculations ---")
    print("Plaintext pairs (numeric):", pairs)

    ciphertext = ""
    for p in pairs:
        vec = np.array(p)
        c = key.dot(vec) % 26
        print(f"{p} × key → {c}")
        ciphertext += num_to_char(c[0]) + num_to_char(c[1])

    return ciphertext

# -----------------------------
# Hill Cipher Decryption
# -----------------------------

def hill_decrypt(ciphertext, key):
    det = int(np.round(np.linalg.det(key))) % 26
    det_inv = mod_inverse(det, 26)

    print("\nDeterminant =", det)
    print("Modular inverse of determinant =", det_inv)

    # Compute adjugate (classical inverse for 2×2)
    adj = np.array([[key[1,1], -key[0,1]],
                    [-key[1,0], key[0,0]]])

    inv_key = (det_inv * adj) % 26
    inv_key = inv_key.astype(int)

    print("\nInverse Key Matrix (mod 26):")
    print(inv_key)

    print("\n--- Decryption Calculations ---")
    ciphertext = ciphertext.lower()
    pairs = []

    for i in range(0, len(ciphertext), 2):
        a = char_to_num(ciphertext[i])
        b = char_to_num(ciphertext[i+1])
        pairs.append([a, b])

    print("Ciphertext pairs (numeric):", pairs)

    plaintext = ""
    for p in pairs:
        vec = np.array(p)
        p_res = inv_key.dot(vec) % 26
        print(f"{p} × inv_key → {p_res}")
        plaintext += num_to_char(p_res[0]) + num_to_char(p_res[1])

    return plaintext


# -----------------------------
# Main Execution
# -----------------------------

message = "meet me at the usual place at ten rather than eight oclock"

# Key matrix
key = np.array([[9,4],
                [5,7]])

cipher = hill_encrypt(message, key)
print("\nCiphertext:", cipher)

plain = hill_decrypt(cipher, key)
print("\nRecovered Plaintext:", plain)
