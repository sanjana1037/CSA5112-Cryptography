import random

# Generate a random OTP key (0–25) for each letter
def generate_key(length):
    return [random.randint(0, 25) for _ in range(length)]

# Encrypt using one-time pad Vigenère
def otp_encrypt(plaintext, key):
    ciphertext = ""
    for i, ch in enumerate(plaintext):
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shift = key[i]
            c = (ord(ch) - base + shift) % 26
            ciphertext += chr(c + base)
        else:
            ciphertext += ch
    return ciphertext

# Decrypt using one-time pad Vigenère
def otp_decrypt(ciphertext, key):
    plaintext = ""
    for i, ch in enumerate(ciphertext):
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shift = key[i]
            p = (ord(ch) - base - shift + 26) % 26
            plaintext += chr(p + base)
        else:
            plaintext += ch
    return plaintext

# ----------------------- MAIN PROGRAM -------------------------
if __name__ == "__main__":
    print("=== One-Time Pad Vigenère Cipher ===")

    plaintext = input("Enter plaintext: ")

    # Generate OTP key length = plaintext length
    key = generate_key(len(plaintext))

    print("\nGenerated One-Time Pad Key (0–25 values):")
    print(key)

    # Encrypt
    ciphertext = otp_encrypt(plaintext, key)
    print("\nCiphertext:", ciphertext)

    # Decrypt
    decrypted = otp_decrypt(ciphertext, key)
    print("Decrypted Plaintext:", decrypted)
