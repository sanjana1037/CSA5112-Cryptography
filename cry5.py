import math

# Function to find modular inverse of 'a' under mod 26
def mod_inverse(a):
    a = a % 26
    for x in range(1, 26):
        if (a * x) % 26 == 1:
            return x
    return None  # No inverse exists

# Function to encrypt
def encrypt(text, a, b):
    result = ""
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            p = ord(ch) - base
            c = (a * p + b) % 26
            result += chr(c + base)
        else:
            result += ch
    return result

# Function to decrypt
def decrypt(cipher, a, b):
    a_inv = mod_inverse(a)
    if a_inv is None:
        return "Error: 'a' has no modular inverse (not coprime with 26). Decryption not possible."
    
    result = ""
    for ch in cipher:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            c = ord(ch) - base
            p = (a_inv * (c - b)) % 26
            result += chr(p + base)
        else:
            result += ch
    return result


# -------- Main Program --------
plaintext = input("Enter the plaintext: ")
a = int(input("Enter value of 'a' (must be coprime with 26): "))
b = int(input("Enter value of 'b': "))

# Check one-to-one condition
if math.gcd(a, 26) != 1:
    print("\nInvalid value of 'a'! It must be coprime with 26 for decryption to work.")
else:
    ciphertext = encrypt(plaintext, a, b)
    print("\nEncrypted text:", ciphertext)

    decrypted = decrypt(ciphertext, a, b)
    print("Decrypted text:", decrypted)
