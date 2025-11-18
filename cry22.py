# -------------------------------
# Helper functions
# -------------------------------
def permute(bits, table):
    return ''.join(bits[i] for i in table)

def xor(a, b):
    return ''.join('1' if a[i] != b[i] else '0' for i in range(len(a)))

def shift_left(bits, n):
    return bits[n:] + bits[:n]

# -------------------------------
# S-Boxes
# -------------------------------
S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2]
]

S1 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3]
]

# -------------------------------
# Key Generation
# -------------------------------
def generate_keys(key10):
    P10 = [2,4,1,6,3,9,0,8,7,5]
    P8  = [5,2,6,3,7,4,9,8]

    key_p10 = permute(key10, P10)

    left = key_p10[:5]
    right = key_p10[5:]

    # K1
    left1 = shift_left(left, 1)
    right1 = shift_left(right, 1)
    K1 = permute(left1 + right1, P8)

    # K2
    left2 = shift_left(left1, 2)
    right2 = shift_left(right1, 2)
    K2 = permute(left2 + right2, P8)

    return K1, K2

# -------------------------------
# Feistel Function
# -------------------------------
def f_k(bits, key):
    EP = [3,0,1,2,1,2,3,0]
    P4 = [1,3,2,0]

    left = bits[:4]
    right = bits[4:]

    expanded = permute(right, EP)
    x = xor(expanded, key)

    left4 = x[:4]
    right4 = x[4:]

    # S0 processing
    r = int(left4[0] + left4[3], 2)
    c = int(left4[1] + left4[2], 2)
    s0val = format(S0[r][c], "02b")

    # S1 processing
    r = int(right4[0] + right4[3], 2)
    c = int(right4[1] + right4[2], 2)
    s1val = format(S1[r][c], "02b")

    out = permute(s0val + s1val, P4)
    return xor(left, out) + right

# -------------------------------
# SDES Encryption / Decryption
# -------------------------------
def sdes_encrypt(pt8, K1, K2):
    IP = [1,5,2,0,3,7,4,6]
    IP_INV = [3,0,2,4,6,1,7,5]

    bits = permute(pt8, IP)
    bits = f_k(bits, K1)
    bits = bits[4:] + bits[:4]
    bits = f_k(bits, K2)
    return permute(bits, IP_INV)

def sdes_decrypt(ct8, K1, K2):
    return sdes_encrypt(ct8, K2, K1)

# -------------------------------
# CBC Mode
# -------------------------------
def CBC_encrypt_block(pt8, prev, K1, K2):
    x = xor(pt8, prev)
    ct = sdes_encrypt(x, K1, K2)
    return ct

def CBC_decrypt_block(ct8, prev, K1, K2):
    x = sdes_decrypt(ct8, K1, K2)
    pt = xor(x, prev)
    return pt

# ----------------------------------------------------
# TEST CASE GIVEN IN QUESTION
# ----------------------------------------------------
IV = "10101010"
P1 = "00000001"
P2 = "00100011"
key10 = "0111111101"

# Generate keys
K1, K2 = generate_keys(key10)

# CBC Encryption
C1 = CBC_encrypt_block(P1, IV, K1, K2)
C2 = CBC_encrypt_block(P2, C1, K1, K2)

# CBC Decryption
D1 = CBC_decrypt_block(C1, IV, K1, K2)
D2 = CBC_decrypt_block(C2, C1, K1, K2)

print("Ciphertext 1:", C1)
print("Ciphertext 2:", C2)
print("Decrypted 1 :", D1)
print("Decrypted 2 :", D2)
