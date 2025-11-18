import math

# Check GCD to ensure one-to-one mapping
def gcd(a, b):
    return math.gcd(a, b)

# Modular inverse of a mod m
def mod_inverse(a, m=26):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# Encrypt: C = (aP + b) mod 26
def affine_encrypt(text, a, b):
    if gcd(a, 26) != 1:
        raise ValueError(f"Invalid 'a' value: {a}. Must be coprime with 26 for one-to-one encryption.")

    cipher = ""
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            p = ord(ch) - base
            c = (a * p + b) % 26
            cipher += chr(c + base)
        else:
            cipher += ch
    return cipher

# Decrypt: P = a_inv (C - b) mod 26
def affine_decrypt(cipher, a, b):
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        raise ValueError(f"'a' = {a} has no modular inverse modulo 26 → decryption impossible.")

    text = ""
    for ch in cipher:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            c = ord(ch) - base
            p = (a_inv * (c - b + 26)) % 26
            text += chr(p + base)
        else:
            text += ch
    return text

# ---------------- MAIN DRIVER ----------------
if __name__ == "__main__":
    print("=== Affine Caesar Cipher ===")
    print("Formula: C = (aP + b) mod 26")
    print("Requirement: gcd(a, 26) must be 1\n")

    print("1. Encrypt")
    print("2. Decrypt")
    choice = int(input("Choose an option: "))

    text = input("Enter text: ")
    a = int(input("Enter value of a: "))
    b = int(input("Enter value of b: "))

    if choice == 1:
        try:
            result = affine_encrypt(text, a, b)
            print("\nCiphertext:", result)
        except ValueError as e:
            print("\nError:", e)

    elif choice == 2:
        try:
            result = affine_decrypt(text, a, b)
            print("\nPlaintext:", result)
        except ValueError as e:
            print("\nError:", e)

    else:
        print("Invalid choice.")
