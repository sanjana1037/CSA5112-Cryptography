# RSA dictionary attack demonstration

# Public key
e = 17
n = 3233    # example RSA modulus (small for demonstration)

# Step 1: Build dictionary for all 26 letters (A=0 ... Z=25)
rsa_dictionary = {}

for m in range(26):
    c = pow(m, e, n)
    rsa_dictionary[c] = m

print("RSA Dictionary (cipher → plaintext):")
print(rsa_dictionary)

# Suppose Alice sends this message encrypted letter-by-letter:
ciphertext = [pow(0, e, n), pow(2, e, n), pow(19, e, n)]  # Example: "ACT"

print("\nCiphertext:", ciphertext)

# Step 2: Attacker decrypts using dictionary (no private key!)
plaintext_numbers = [rsa_dictionary[c] for c in ciphertext]

# Convert numbers back to letters
plaintext = ''.join(chr(num + 65) for num in plaintext_numbers)

print("\nDecrypted message:", plaintext)
