# -------------------------------------------------------
# ECB vs CBC Error Propagation Demonstration (Python)
# -------------------------------------------------------

def encrypt_block(p, key):
    """Toy encryption: XOR with key"""
    return p ^ key

def decrypt_block(c, key):
    """Toy decryption: XOR with key"""
    return c ^ key


# ------------------- Original blocks --------------------
P = [0x10, 0x20, 0x30]  # plaintext blocks
key = 0xAA             # toy key
IV  = 0x55             # CBC IV

print("Original Plaintext Blocks:", [hex(x) for x in P])


# =======================================================
#                    ECB MODE
# =======================================================

# Encrypt
C_ecb = [encrypt_block(p, key) for p in P]

# Introduce error in the first ciphertext block C1
C_ecb[0] ^= 0x01

# Decrypt
D_ecb = [decrypt_block(c, key) for c in C_ecb]

print("\nECB Mode Results:")
print("Decrypted Plaintext:", [hex(x) for x in D_ecb])
print("Observation: Only P1 is corrupted. P2 and P3 are correct.")


# =======================================================
#                    CBC MODE
# =======================================================

# CBC Encryption
C_cbc = []
prev = IV

for p in P:
    c = encrypt_block(p ^ prev, key)
    C_cbc.append(c)
    prev = c

# Introduce error in ciphertext block C1
C_cbc[0] ^= 0x01

# CBC Decryption
D_cbc = []
prev = IV
for c in C_cbc:
    p = decrypt_block(c, key) ^ prev
    D_cbc.append(p)
    prev = c

print("\nCBC Mode Results after error in C1:")
print("Decrypted Plaintext:", [hex(x) for x in D_cbc])
print("Observation: P1 and P2 are corrupted. No other blocks affected.")


# =======================================================
#      ERROR IN PLAINTEXT BEFORE CBC ENCRYPTION
# =======================================================

# Introduce bit error in plaintext P1
P_err = P.copy()
P_err[0] ^= 0x01  # flip a bit

# CBC Encryption with erroneous plaintext
C_pErr = []
prev = IV

for p in P_err:
    c = encrypt_block(p ^ prev, key)
    C_pErr.append(c)
    prev = c

print("\nCBC Encryption when plaintext P1 has a bit error:")
print("Ciphertext blocks:", [hex(x) for x in C_pErr])
print("Observation: Only ciphertext block C1 is affected.")
