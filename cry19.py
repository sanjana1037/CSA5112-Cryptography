from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# ---------------------------
# 3DES Encryption in CBC Mode
# ---------------------------

# Sample 24-byte key (3DES uses 16 or 24 bytes)
key = get_random_bytes(24)

# Initialization vector (8 bytes for DES/3DES block)
iv = get_random_bytes(8)

# Plaintext (must be multiple of block size after padding)
plaintext = b"Hello, this is a secret message for CBC mode testing!"

# Pad plaintext to 8-byte blocks
padded_plaintext = pad(plaintext, DES3.block_size)

# Create cipher object
cipher = DES3.new(key, DES3.MODE_CBC, iv)

# Encrypt
ciphertext = cipher.encrypt(padded_plaintext)

print("3DES CBC Encryption")
print("------------------")
print("Key (hex):       ", key.hex())
print("IV (hex):        ", iv.hex())
print("Ciphertext (hex):", ciphertext.hex())

# ---------------------------
# Decryption
# ---------------------------
decipher = DES3.new(key, DES3.MODE_CBC, iv)
decrypted = unpad(decipher.decrypt(ciphertext), DES3.block_size)

print("\nDecrypted plaintext:", decrypted.decode())
