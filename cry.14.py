import string

alphabet = string.ascii_lowercase

# -------------------------
# PART (A): Encryption
# -------------------------
plaintext = "send more money".replace(" ", "")
key_stream = [9,0,1,7,23,15,21,14,11,11,2,8,9]

ciphertext = ""
for p, k in zip(plaintext, key_stream):
    c = (alphabet.index(p) + k) % 26
    ciphertext += alphabet[c]

print("Ciphertext:", ciphertext)

# -------------------------
# PART (B): Find key so ciphertext decrypts to new plaintext
# -------------------------
new_plain = "cash not needed".replace(" ", "")

# Ensure same length constraint
if len(new_plain) != len(ciphertext):
    print("Error: Text lengths do not match for OTP decryption!")
else:
    recovered_key = []
    for c, p in zip(ciphertext, new_plain):
        k = (alphabet.index(c) - alphabet.index(p)) % 26
        recovered_key.append(k)

    print("Recovered Key for new plaintext:")
    print(recovered_key)
