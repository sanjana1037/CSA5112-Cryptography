import string
import random
import math

alphabet = string.ascii_lowercase

# English letter frequency (ETAOIN SHRDLU order)
english_freq_order = "etaoinshrdlcumwfgypbvkjxqz"

def score_text(text):
    """Score text based on English letter frequencies."""
    freq = {c: 0 for c in alphabet}
    total = 0
    
    for ch in text:
        if ch in alphabet:
            freq[ch] += 1
            total += 1

    if total == 0:
        return 0.0

    score = 0
    for c in alphabet:
        score += (freq[c] / total) * (english_freq_order.index(c) + 1)
    
    return score

def decrypt(cipher, key_map):
    """Apply substitution key map."""
    result = ""
    for ch in cipher:
        if ch in alphabet:
            result += key_map[ch]
        else:
            result += ch
    return result

def generate_initial_key(cipher):
    """Frequency-based initial guess."""
    freq = {c: 0 for c in alphabet}
    for ch in cipher:
        if ch in alphabet:
            freq[ch] += 1

    sorted_cipher_letters = sorted(freq, key=freq.get, reverse=True)

    key_map = {}
    for ciph, eng in zip(sorted_cipher_letters, english_freq_order):
        key_map[ciph] = eng

    # Fill remaining letters
    remaining = [c for c in alphabet if c not in key_map.values()]
    unmapped = [c for c in alphabet if c not in key_map]
    
    for c, r in zip(unmapped, remaining):
        key_map[c] = r
    
    return key_map

def mutate_key(key_map):
    """Randomly swap two letters in the key."""
    new_key = key_map.copy()
    a, b = random.sample(alphabet, 2)
    
    # swap values
    new_key = new_key.copy()
    new_key[a], new_key[b] = new_key[b], new_key[a]
    return new_key

def frequency_attack(cipher, top_n=10, iterations=20000):
    results = []

    # Initial guess
    key = generate_initial_key(cipher)
    plaintext = decrypt(cipher, key)
    best_score = score_text(plaintext)
    
    results.append((best_score, plaintext))

    for _ in range(iterations):
        new_key = mutate_key(key)
        new_plain = decrypt(cipher, new_key)
        new_score = score_text(new_plain)

        # Hill climbing – accept if better
        if new_score > best_score:
            key = new_key
            best_score = new_score
            plaintext = new_plain
            results.append((best_score, plaintext))

    # Sort by score descending
    results = sorted(results, key=lambda x: x[0], reverse=True)

    # Deduplicate plaintexts
    seen = set()
    final_results = []
    for score, text in results:
        if text not in seen:
            seen.add(text)
            final_results.append((score, text))
            if len(final_results) >= top_n:
                break

    return final_results

# -----------------------------
# MAIN PROGRAM
# -----------------------------
ciphertext = input("Enter monoalphabetic substitution ciphertext: ").lower()
top_n = int(input("How many top plaintexts do you want? "))

print(f"\nTrying to break substitution cipher…\n")

candidates = frequency_attack(ciphertext, top_n)

print(f"\nTop {top_n} candidate plaintexts:\n")
for i, (score, text) in enumerate(candidates, 1):
    print(f"[Rank {i}]  Score = {score:.3f}")
    print(" ", text)
    print()
