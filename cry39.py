import string

# English letter frequency order (most → least common)
english_freq_order = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

def decrypt_additive(ciphertext, key):
    """
    Decrypt additive cipher where:
    P = (C - key) mod 26
    """
    plaintext = ""
    for ch in ciphertext.upper():
        if 'A' <= ch <= 'Z':
            p = (ord(ch) - ord('A') - key) % 26
            plaintext += chr(p + ord('A'))
        else:
            plaintext += ch
    return plaintext


def score_text(text):
    """
    Score based on frequency resemblance to English.
    Lower score → more likely.
    """
    freq = {ch: 0 for ch in string.ascii_uppercase}

    for ch in text:
        if ch in freq:
            freq[ch] += 1

    sorted_text_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    ranked = ''.join([x[0] for x in sorted_text_freq])

    score = 0
    for i, ch in enumerate(ranked):
        score += abs(i - english_freq_order.index(ch))

    return score


def attack(ciphertext, top_n=10):
    results = []

    for key in range(26):
        plaintext = decrypt_additive(ciphertext, key)
        score_val = score_text(plaintext)
        results.append((score_val, key, plaintext))

    # Sort by score
    results.sort(key=lambda x: x[0])

    print(f"\n=== Top {top_n} Most Likely Plaintexts ===\n")
    for i in range(min(top_n, len(results))):
        score_val, key, plaintext = results[i]
        print(f"[{i+1}] Key = {key}  | Score = {score_val}")
        print(plaintext)
        print("-" * 50)


# ----------------- Main Program ------------------
if __name__ == "__main__":
    print("Additive Cipher Frequency Attack (Automatic)")

    ciphertext = input("Enter ciphertext: ")
    top_n = int(input("How many top plaintexts to display? "))

    attack(ciphertext, top_n)
