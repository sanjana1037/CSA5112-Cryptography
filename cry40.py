import string
from itertools import permutations

# English letter frequency order (most→least frequent)
english_freq_order = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

def score_text(text):
    """
    Score a plaintext candidate by how closely its letter-frequency
    distribution resembles English.
    """
    text = text.upper()
    freq = {ch: 0 for ch in string.ascii_uppercase}
    for ch in text:
        if ch in freq:
            freq[ch] += 1

    sorted_text_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    ranked_letters = ''.join([x[0] for x in sorted_text_freq])
    
    score = 0
    for i, ch in enumerate(ranked_letters):
        score += abs(i - english_freq_order.index(ch))
    return score


def substitute(ciphertext, mapping):
    result = ""
    for ch in ciphertext.upper():
        if ch in mapping:
            result += mapping[ch]
        else:
            result += ch
    return result


def attack(ciphertext, top_n=10):
    # Count frequencies in ciphertext
    freq = {ch: 0 for ch in string.ascii_uppercase}
    for ch in ciphertext.upper():
        if ch in freq:
            freq[ch] += 1

    sorted_cipher = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    cipher_freq_order = ''.join([x[0] for x in sorted_cipher])

    # Try permutations of the top 6 letters for better accuracy
    likely_plaintexts = []
    top_cipher_letters = cipher_freq_order[:6]
    top_english_letters = english_freq_order[:6]

    for perm in permutations(top_english_letters):
        mapping = {}
        
        for i, ch in enumerate(top_cipher_letters):
            mapping[ch] = perm[i]

        # Fill the rest deterministically
        for i, ch in enumerate(cipher_freq_order[6:]):
            mapping[ch] = english_freq_order[6 + i]

        plaintext = substitute(ciphertext, mapping)
        score_val = score_text(plaintext)
        likely_plaintexts.append((score_val, plaintext))

    # Sort by score (lower is better)
    likely_plaintexts.sort(key=lambda x: x[0])

    print("\n=== TOP", top_n, "PLAINTEXT GUESSES ===\n")
    for i in range(min(top_n, len(likely_plaintexts))):
        print(f"[{i+1}] Score={likely_plaintexts[i][0]}")
        print(likely_plaintexts[i][1])
        print("-" * 50)


# ---------------- MAIN PROGRAM ----------------
if __name__ == "__main__":
    print("Monoalphabetic Substitution Cipher Frequency Attack")
    ciphertext = input("Enter ciphertext: ")
    top = int(input("How many top plaintexts to show? "))

    attack(ciphertext, top)
