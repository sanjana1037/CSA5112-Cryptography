import os

BLOCK_SIZE = 8  # block size in bytes

# -------------------- Padding --------------------
def pad(data):
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    if pad_len == 0:
        pad_len = BLOCK_SIZE
    return data + bytes([0x80] + [0x00]*(pad_len-1))

def unpad(data):
    # Remove padding: last 0x80 followed by zeros
    if not data:
        return data
    i = len(data) - 1
    while i >= 0 and data[i] == 0x00:
        i -= 1
    if i >= 0 and data[i] == 0x80:
        return data[:i]
    return data

# -------------------- ECB Mode --------------------
def ecb_encrypt(plaintext, key):
    ciphertext = bytearray()
    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i+BLOCK_SIZE]
        ciphertext.extend(bytes([b ^ k for b, k in zip(block, key)]))
    return ciphertext

def ecb_decrypt(ciphertext, key):
    return ecb_encrypt(ciphertext, key)  # XOR symmetric

# -------------------- CBC Mode --------------------
def cbc_encrypt(plaintext, key, iv):
    ciphertext = bytearray()
    prev = iv
    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = bytes([b ^ p for b, p in zip(plaintext[i:i+BLOCK_SIZE], prev)])
        enc_block = bytes([b ^ k for b, k in zip(block, key)])
        ciphertext.extend(enc_block)
        prev = enc_block
    return ciphertext

def cbc_decrypt(ciphertext, key, iv):
    plaintext = bytearray()
    prev = iv
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i+BLOCK_SIZE]
        dec_block = bytes([b ^ k for b, k in zip(block, key)])
        plaintext.extend(bytes([b ^ p for b, p in zip(dec_block, prev)]))
        prev = block
    return plaintext

# -------------------- CFB Mode --------------------
def cfb_encrypt(plaintext, key, iv):
    ciphertext = bytearray()
    feedback = iv
    for i in range(0, len(plaintext), BLOCK_SIZE):
        temp = bytes([f ^ k for f, k in zip(feedback, key)])
        block = plaintext[i:i+BLOCK_SIZE]
        enc_block = bytes([b ^ t for b, t in zip(block, temp)])
        ciphertext.extend(enc_block)
        feedback = enc_block
    return ciphertext

def cfb_decrypt(ciphertext, key, iv):
    plaintext = bytearray()
    feedback = iv
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        temp = bytes([f ^ k for f, k in zip(feedback, key)])
        block = ciphertext[i:i+BLOCK_SIZE]
        dec_block = bytes([b ^ t for b, t in zip(block, temp)])
        plaintext.extend(dec_block)
        feedback = block
    return plaintext

# -------------------- Example Usage --------------------
if __name__ == "__main__":
    plaintext = b"HELLO WORLD! THIS IS A TEST MESSAGE."
    key = os.urandom(BLOCK_SIZE)
    iv = os.urandom(BLOCK_SIZE)

    print("Original Plaintext:", plaintext)

    # Padding
    padded = pad(plaintext)

    # ECB
    ecb_ct = ecb_encrypt(padded, key)
    print("ECB Ciphertext:", ecb_ct)
    print("ECB Decrypted:", unpad(ecb_decrypt(ecb_ct, key)))

    # CBC
    cbc_ct = cbc_encrypt(padded, key, iv)
    print("CBC Ciphertext:", cbc_ct)
    print("CBC Decrypted:", unpad(cbc_decrypt(cbc_ct, key, iv)))

    # CFB
    cfb_ct = cfb_encrypt(padded, key, iv)
    print("CFB Ciphertext:", cfb_ct)
    print("CFB Decrypted:", unpad(cfb_decrypt(cfb_ct, key, iv)))
