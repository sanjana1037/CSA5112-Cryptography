from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


# -------------------------------------------------------
# 1. Custom Padding (1-bit followed by zeros)
# -------------------------------------------------------
def pad_message(data, block_size=16):
    pad_len = block_size - (len(data) % block_size)
    if pad_len == 0:
        pad_len = block_size    # Add full padding block even if already aligned
    
    # 1 bit -> 0x80 (1000 0000), rest zeros
    padding = bytes([0x80]) + bytes(pad_len - 1)
    return data + padding


def unpad_message(data):
    # Remove padding: scan backwards to find 0x80
    i = len(data) - 1
    while i >= 0 and data[i] == 0:
        i -= 1
    if data[i] == 0x80:
        return data[:i]
    return data  # No padding found


# -------------------------------------------------------
# 2. ECB Encryption/Decryption
# -------------------------------------------------------
def aes_ecb_encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_ECB)
    padded = pad_message(plaintext)
    return cipher.encrypt(padded)

def aes_ecb_decrypt(key, ciphertext):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    return unpad_message(decrypted)


# -------------------------------------------------------
# 3. CBC Encryption/Decryption
# -------------------------------------------------------
def aes_cbc_encrypt(key, plaintext, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad_message(plaintext)
    return cipher.encrypt(padded)

def aes_cbc_decrypt(key, ciphertext, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    return unpad_message(decrypted)


# -------------------------------------------------------
# 4. CFB Encryption/Decryption (no padding needed)
# -------------------------------------------------------
def aes_cfb_encrypt(key, plaintext, iv):
    cipher = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
    return cipher.encrypt(plaintext)

def aes_cfb_decrypt(key, ciphertext, iv):
    cipher = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
    return cipher.decrypt(ciphertext)


# -------------------------------------------------------
# 5. Test Program
# -------------------------------------------------------
if __name__ == "__main__":
    key = get_random_bytes(16)
    iv = get_random_bytes(16)

    plaintext = b"HELLO WORLD AES TEST"

    print("\nOriginal Plaintext:", plaintext)

    # ---------- ECB ----------
    e_ecb = aes_ecb_encrypt(key, plaintext)
    d_ecb = aes_ecb_decrypt(key, e_ecb)

    print("\nECB Encrypted:", e_ecb)
    print("ECB Decrypted:", d_ecb)

    # ---------- CBC ----------
    e_cbc = aes_cbc_encrypt(key, plaintext, iv)
    d_cbc = aes_cbc_decrypt(key, e_cbc, iv)

    print("\nCBC Encrypted:", e_cbc)
    print("CBC Decrypted:", d_cbc)

    # ---------- CFB ----------
    e_cfb = aes_cfb_encrypt(key, plaintext, iv)
    d_cfb = aes_cfb_decrypt(key, e_cfb, iv)

    print("\nCFB Encrypted:", e_cfb)
    print("CFB Decrypted:", d_cfb)
