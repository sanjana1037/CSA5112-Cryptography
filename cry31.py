from Crypto.Cipher import AES

# ------------------------- Helper Functions -------------------------

def xor_bytes(a: bytes, b: bytes) -> bytes:
    """XOR two byte strings"""
    return bytes([x ^ y for x, y in zip(a, b)])

def left_shift(bits: bytes) -> bytes:
    """Left shift a byte string by 1 bit"""
    shifted = int.from_bytes(bits, 'big') << 1
    shifted &= (1 << (len(bits) * 8)) - 1  # Mask to original length
    return shifted.to_bytes(len(bits), 'big')

# -------------------- CMAC Subkey Generation -----------------------

def generate_cmac_subkeys(key: bytes, block_size: int = 16):
    """
    Generate K1 and K2 subkeys for CMAC
    :param key: AES key
    :param block_size: block size in bytes (16 for AES-128, 8 for DES)
    """
    # Constants for CMAC
    if block_size == 16:  # 128-bit block
        const_Rb = bytes.fromhex('00000000000000000000000000000087')
    elif block_size == 8:  # 64-bit block
        const_Rb = bytes.fromhex('000000000000001B')
    else:
        raise ValueError("Unsupported block size")

    # 1. Encrypt 0-block with AES
    cipher = AES.new(key, AES.MODE_ECB)
    L = cipher.encrypt(bytes([0] * block_size))

    # 2. Generate K1
    K1 = left_shift(L)
    if (L[0] & 0x80):  # if MSB = 1
        K1 = xor_bytes(K1, const_Rb)

    # 3. Generate K2
    K2 = left_shift(K1)
    if (K1[0] & 0x80):  # if MSB = 1
        K2 = xor_bytes(K2, const_Rb)

    return K1, K2

# ----------------------- Example Usage -----------------------
if __name__ == "__main__":
    key = b'This is a key123'  # 16-byte AES key
    K1, K2 = generate_cmac_subkeys(key, 16)

    print("Subkey K1:", K1.hex())
    print("Subkey K2:", K2.hex())
