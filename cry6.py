def modinv(a, m=26):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# Given clues
c1, c2 = ord('B') - 65, ord('U') - 65   # ciphertext letters
p1, p2 = ord('E') - 65, ord('T') - 65   # plaintext guesses

# Solve for a and b
a = ((c1 - c2) * modinv(p1 - p2)) % 26
b = (c1 - a * p1) % 26
ainv = modinv(a)

print(f"Keys found: a={a}, b={b}")

text = input("Enter ciphertext: ").upper()
plain = ""

for ch in text:
    if ch.isalpha():
        p = (ainv * (ord(ch) - 65 - b)) % 26
        plain += chr(p + 65)
    else:
        plain += ch

print("Decrypted text:", plain)
