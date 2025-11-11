def generate_key(plaintext, key):
    key = key.lower()
    key = list(key)
    if len(plaintext) == len(key):
        return key
    else:
        for i in range(len(plaintext) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)


def encrypt(plaintext, key):
    ciphertext = []
    for p, k in zip(plaintext, key):
        if p.isalpha():
            shift = ord(k) - ord('a')
            if p.isupper():
                ciphertext.append(chr((ord(p) - 65 + shift) % 26 + 65))
            else:
                ciphertext.append(chr((ord(p) - 97 + shift) % 26 + 97))
        else:
            ciphertext.append(p)
    return "".join(ciphertext)


def decrypt(ciphertext, key):
    plaintext = []
    for c, k in zip(ciphertext, key):
        if c.isalpha():
            shift = ord(k) - ord('a')
            if c.isupper():
                plaintext.append(chr((ord(c) - 65 - shift) % 26 + 65))
            else:
                plaintext.append(chr((ord(c) - 97 - shift) % 26 + 97))
        else:
            plaintext.append(c)
    return "".join(plaintext)


# ---------- MAIN PROGRAM ----------
plaintext = input("Enter the plaintext: ")
key_input = input("Enter the key: ")

key = generate_key(plaintext, key_input)

ciphertext = encrypt(plaintext, key)
print("\nEncrypted text:", ciphertext)

decrypted = decrypt(ciphertext, key)
print("Decrypted text:", decrypted)
