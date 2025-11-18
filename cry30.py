from Crypto.Cipher import AES

# ------------------------- Helper Functions -------------------------
def xor_bytes(a: bytes, b: bytes) -> bytes:
    """XOR two byte strings"""
    return bytes([x ^ y for x, y in zip(a, b)])

# ------------------------- CBC-MAC Implementation -------------------------
def cbc_mac(key: bytes, message: bytes) -> bytes:
    """
    Compute CBC-MAC of a message (assume full blocks)
    :param key: AES key
    :param message: bytes, must be multiple of block size
    """
    block_size = 16
    cipher = AES.new(key, AES.MODE_ECB)
    if len(message) % block_size != 0:
        raise ValueError("Message must be multiple of block size")

    prev = bytes([0] * block_size)
    for i in range(0, len(message), block_size):
        block = message[i:i+block_size]
        prev = cipher.encrypt(xor_bytes(block, prev))
    return prev

# ------------------------- Demonstration -------------------------
if __name__ == "__main__":
    key = b'This is a key123'  # 16-byte AES key
    block_size = 16

    # One-block message X
    X = b'Attack at dawn!!'  # 16 bytes

    # CBC-MAC of one-block message
    T = cbc_mac(key, X)
    print("CBC-MAC of one-block X:", T.hex())

    # Construct two-block message X || (X ⊕ T)
    X2 = xor_bytes(X, T)
    two_block_message = X + X2

    # CBC-MAC of two-block message
    T2 = cbc_mac(key, two_block_message)
    print("CBC-MAC of two-block X || (X ⊕ T):", T2.hex())

    # Verify attack property
    print("T2 equals T?", T2 == T)
