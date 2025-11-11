import string
import random

# Generate random substitution alphabet
def generate_key():
    letters = list(string.ascii_lowercase)
    shuffled = letters.copy()
    random.shuffle(shuffled)
    return dict(zip(letters, shuffled))

# Encrypt the message
def encrypt(plaintext, key):
    ciphertext = ""
    for char in plaintext.lower():
        if char in key:
            ciphertext += key[char]
        else:
            ciphertext += char  # Keep spaces, punctuation, etc.
    return ciphertext

# Decrypt the message
def decrypt(ciphertext, key):
    reversed_key = {v: k for k, v in key.items()}
    plaintext = ""
    for char in ciphertext.lower():
        if char in reversed_key:
            plaintext += reversed_key[char]
        else:
            plaintext += char
    return plaintext


# Main program
plaintext = input("Enter the message to encrypt: ")

# Generate a random key (mapping)
key = generate_key()
print("\nMonoalphabetic Key Mapping:")
for p, c in key.items():
    print(f"{p} -> {c}")

ciphertext = encrypt(plaintext, key)
print("\nEncrypted message:", ciphertext)

decrypted = decrypt(ciphertext, key)
print("Decrypted message:", decrypted)
