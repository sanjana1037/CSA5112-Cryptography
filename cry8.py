def generate_cipher(keyword):
    keyword = keyword.upper()
    used = set()
    cipher = []

    # Add keyword letters first
    for ch in keyword:
        if ch.isalpha() and ch not in used:
            cipher.append(ch)
            used.add(ch)

    # Add remaining letters
    for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if ch not in used:
            cipher.append(ch)

    return ''.join(cipher)

def encrypt(plaintext, cipher):
    plaintext = plaintext.upper()
    result = ""
    for ch in plaintext:
        if ch.isalpha():
            idx = ord(ch) - ord('A')
            result += cipher[idx]
        else:
            result += ch
    return result

def decrypt(ciphertext, cipher):
    ciphertext = ciphertext.upper()
    result = ""
    for ch in ciphertext:
        if ch.isalpha():
            idx = cipher.index(ch)
            result += chr(idx + ord('A'))
        else:
            result += ch
    return result

# --- Main Program ---
keyword = input("Enter the keyword: ")
cipher = generate_cipher(keyword)
print(f"Cipher alphabet: {cipher}")

plaintext = input("Enter the plaintext: ")
ciphertext = encrypt(plaintext, cipher)
print(f"Encrypted text: {ciphertext}")

ciphertext_input = input("Enter ciphertext to decrypt: ")
decrypted = decrypt(ciphertext_input, cipher)
print(f"Decrypted text: {decrypted}")
