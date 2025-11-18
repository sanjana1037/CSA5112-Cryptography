# ----------------------------------------------------
#  DES With Modified Subkey Rules (24 bits + 24 bits)
# ----------------------------------------------------

# Left circular shift for a 28‑bit value
def left_shift(bits, n):
    return bits[n:] + bits[:n]

# DES Expansion (E-Box)
EBOX = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9,10,11,12,13,
   12,13,14,15,16,17,
   16,17,18,19,20,21,
   20,21,22,23,24,25,
   24,25,26,27,28,29,
   28,29,30,31,32,1
]

# Simple XOR
def xor(a, b):
    return ''.join('0' if x==y else '1' for x,y in zip(a,b))

# Simple S-box: (NOT real DES S-box, simplified)
def sbox_6_to_4(bits):
    # Take 6 bits → return 4 bits using a dummy mapping
    # This is *NOT REAL DES*, only for demonstration
    v = int(bits, 2)
    return format((v * 7) % 16, '04b')

def f_function(R, K):
    # Expand R from 32 → 48 bits
    expanded = ''.join(R[i-1] for i in EBOX)

    # XOR with subkey
    xored = xor(expanded, K)

    # Apply dummy S-box, converting 48 → 32
    out = ""
    for i in range(0, 48, 6):
        out += sbox_6_to_4(xored[i:i+6])

    return out  # 32 bits

# ----------------------------------------------------
#  Subkey Generation: 24 bits from L, 24 bits from R
# ----------------------------------------------------

# Standard DES shift schedule
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2,
                  1, 2, 2, 2, 2, 2, 2, 1]

def generate_subkeys(initial_key56):
    L = initial_key56[:28]
    R = initial_key56[28:]

    subkeys = []

    for i in range(16):
        # Perform defined circular shifts
        L = left_shift(L, SHIFT_SCHEDULE[i])
        R = left_shift(R, SHIFT_SCHEDULE[i])

        # Take first 24 bits of L and first 24 bits of R → 48-bit key
        Ki = L[:24] + R[:24]
        subkeys.append(Ki)

    return subkeys

# ----------------------------------------------------
#  16-Round DES Encryption
# ----------------------------------------------------
def des_encrypt(plaintext64, key56):

    # Generate 16 subkeys
    subkeys = generate_subkeys(key56)

    # Split plain text
    L = plaintext64[:32]
    R = plaintext64[32:]

    # 16 Feistel rounds
    for i in range(16):
        newL = R
        newR = xor(L, f_function(R, subkeys[i]))
        L, R = newL, newR

    # Swap L and R
    return R + L

# ----------------------------------------------------
# Example Input
# ----------------------------------------------------
if __name__ == "__main__":
    # 64-bit plaintext
    plaintext = "0001001000110100010101100111100010011010101111001101111011110001"

    # 56-bit key
    key = "00010011001101000101011101111001100110101011110011001101"

    ciphertext = des_encrypt(plaintext, key)

    print("Plaintext:  ", plaintext)
    print("Key (56b):  ", key)
    print("Ciphertext: ", ciphertext)
