import string

# English letter frequency (approximate)
english_freq = {
    'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7,
    's': 6.3, 'h': 6.1, 'r': 6.0, 'd': 4.3, 'l': 4.0, 'c': 2.8,
    'u': 2.8, 'm': 2.4, 'w': 2.4, 'f': 2.2, 'g': 2.0, 'y': 2.0,
    'p': 1.9, 'b': 1.5, 'v': 1.0, 'k': 0.8, 'j': 0.15, 'x': 0.15,
    'q': 0.10, 'z': 0.07
}

alphabet = string.ascii_lowercase

# -----------------------------
# Caesar Decrypt with key k
# -----------------------------
def decrypt(cipher, k):
    plain = ""
    for ch in cipher:
        if ch in alphabet:
            plain += alphabet[(alphabet.index(ch) - k) % 26]
        else:
            plain += ch
    return plain

# -----------------------------
# Score plaintext by frequency
# -----------------------------
def score_text(text):
    score = 0
    for ch in text:
        if ch in english_freq:
            score += english_freq[ch]
    return score

# -----------------------------
# Frequency Attack
# -----------------------------
def frequency_attack(cipher, top_n=10):
    results = []

    for key in range(26):
        plain = decrypt(cipher, key)
        score = score_text(plain)
        results.append((score, key, plain))

    # Sort highest score → most likely
    results.sort(reverse=True)

    print(f"\nTop {top_n} most likely plaintexts:\n")
    for i in range(top_n):
        score, key, plaintext = results[i]
        print(f"[Rank {i+1}]  Key = {key:2d}   Score = {score:.2f}")
        print(" ", plaintext)
        print()

# -----------------------------
# MAIN
# -----------------------------
ciphertext = input("Enter additive cipher text: ").lower()
top_n = int(input("How many top plaintexts do you want? "))

frequency_attack(ciphertext, top_n)
