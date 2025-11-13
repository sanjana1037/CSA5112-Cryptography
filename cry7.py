# simple_substitution_decrypt.py

ciphertext = input("Enter the ciphertext:\n")

# Define your substitution key mapping here:
# Example: replace symbols/numbers with letters you know or guess.
mapping = {
    '‡': 'E', '†': 'T', '¶': 'H', '(': 'A', ')': 'N', '*': 'D', ';': 'O',
    '4': 'R', '8': 'S', '6': 'I', '5': 'L', '3': 'C', '0': 'U', '9': 'M',
    '2': 'Y', '1': 'B', ':': 'G', '?': 'F', ']': 'W', '—': 'P'
}

plaintext = ""
for ch in ciphertext:
    if ch in mapping:
        plaintext += mapping[ch]
    else:
        plaintext += ch  # keep symbols not in mapping as-is

print("\nDecrypted text:\n", plaintext)
