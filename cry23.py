# -----------------------------
#     S-DES CTR Mode in Python
# -----------------------------

# Permutation functions
def permute(bits, p):
    return ''.join(bits[i-1] for i in p)

def left_shift(bits, n):
    return bits[n:] + bits[:n]

# S-DES Key Generation
def generate_keys(key):
    P10 = [3,5,2,7,4,10,1,9,8,6]
    P8  = [6,3,7,4,8,5,10,9]

    key_p10 = permute(key, P10)
    left = key_p10[:5]
    right = key_p10[5:]

    # Round 1
    left1 = left_shift(left, 1)
    right1 = left_shift(right, 1)
    K1 = permute(left1 + right1, P8)

    # Round 2
    left2 = left_shift(left1, 2)
    right2 = left_shift(right1, 2)
    K2 = permute(left2 + right2, P8)

    return K1, K2

# S-Boxes
S0 = [
    [1,0,3,2],
    [3,2,1,0],
    [0,2,1,3],
    [3,1,3,2]
]

S1 = [
    [0,1,2,3],
    [2,0,1,3],
    [3,0,1,0],
    [2,1,0,3]
]

def sbox_lookup(bits, sbox):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    return format(sbox[row][col], '02b')

def fk(bits, key):
    EP = [4,1,2,3,2,3,4,1]
    P4 = [2,4,3,1]

    left = bits[:4]
    right = bits[4:]

    right_expanded = permute(right, EP)
    xored = format(int(right_expanded, 2) ^ int(key, 2), '08b')

    left4 = sbox_lookup(xored[:4], S0)
    right4 = sbox_lookup(xored[4:], S1)

    p4_bits = permute(left4 + right4, P4)
    left_result = format(int(left, 2) ^ int(p4_bits, 2), '04b')

    return left_result + right

def sdes_encrypt_block(plain, K1, K2):
    IP = [2,6,3,1,4,8,5,7]
    IP_inv = [4,1,3,5,7,2,8,6]

    temp = permute(plain, IP)
    temp = fk(temp, K1)
    temp = temp[4:] + temp[:4]  # Swap
    temp = fk(temp, K2)
    cipher = permute(temp, IP_inv)
    return cipher

def sdes_ctr_encrypt(plaintext, key, counter_start="00000000"):
    K1, K2 = generate_keys(key)

    blocks = [plaintext[i:i+8] for i in range(0, len(plaintext), 8)]
    counter = int(counter_start, 2)

    ciphertext = ""

    for block in blocks:
        ctr_bits = format(counter, '08b')
        encrypted_ctr = sdes_encrypt_block(ctr_bits, K1, K2)
        cipher_block = format(int(block, 2) ^ int(encrypted_ctr, 2), '08b')
        ciphertext += cipher_block
        counter += 1

    return ciphertext

def sdes_ctr_decrypt(ciphertext, key, counter_start="00000000"):
    return sdes_ctr_encrypt(ciphertext, key, counter_start)


# ------------------------------------------------------
# TEST CASE FROM QUESTION
# ------------------------------------------------------

key = "0111111101"
plaintext = "000000010000001000000100"  # 3 blocks
counter_start = "00000000"

cipher = sdes_ctr_encrypt(plaintext, key, counter_start)
plain2 = sdes_ctr_decrypt(cipher, key, counter_start)

print("Plaintext :", plaintext)
print("Ciphertext:", cipher)
print("Decrypted :", plain2)
