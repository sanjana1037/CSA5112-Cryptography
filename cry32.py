from Crypto.PublicKey import DSA, RSA
from Crypto.Signature import DSS, pkcs1_15
from Crypto.Hash import SHA256
import os

# ----------------------- Message -----------------------
message = b"Important message"

# ----------------------- DSA Signatures -----------------------
# Generate DSA key
dsa_key = DSA.generate(1024)
h = SHA256.new(message)

# Use DSS to sign (k is generated internally each time)
signer = DSS.new(dsa_key, 'fips-186-3')
signature1 = signer.sign(h)
signature2 = signer.sign(h)

print("DSA Signatures for the same message (different each time):")
print(signature1.hex())
print(signature2.hex())
print("Are DSA signatures equal?", signature1 == signature2)

# ----------------------- RSA Signatures -----------------------
# Generate RSA key
rsa_key = RSA.generate(1024)
h_rsa = SHA256.new(message)

signature_rsa1 = pkcs1_15.new(rsa_key).sign(h_rsa)
signature_rsa2 = pkcs1_15.new(rsa_key).sign(h_rsa)

print("\nRSA Signatures for the same message (identical each time):")
print(signature_rsa1.hex())
print(signature_rsa2.hex())
print("Are RSA signatures equal?", signature_rsa1 == signature_rsa2)
