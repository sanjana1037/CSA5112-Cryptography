# ---------------------------------------------------------
# Diffie–Hellman Demonstration for Q28
# ---------------------------------------------------------

import random

# -------------------------------
# Function: modular exponentiation
# -------------------------------
def modexp(base, exp, mod):
    return pow(base, exp, mod)

# --------------------------------------------------
# Normal Diffie–Hellman Key Exchange
# --------------------------------------------------
def normal_dh(a, q, xA, xB):
    print("\n--- NORMAL DIFFIE–HELLMAN ---")

    # Values sent publicly
    A = modexp(a, xA, q)
    B = modexp(a, xB, q)

    print(f"Alice sends: {A}")
    print(f"Bob sends  : {B}")

    # Shared key
    keyA = modexp(B, xA, q)
    keyB = modexp(A, xB, q)

    print(f"Alice computes key: {keyA}")
    print(f"Bob computes key   : {keyB}")

    return keyA, keyB


# --------------------------------------------------
# WRONG METHOD: Sending x^a mod q instead of a^x mod q
# --------------------------------------------------
def wrong_method(a, q, xA, xB):
    print("\n--- WRONG METHOD (sending x^a mod q) ---")

    A_wrong = modexp(xA, a, q)
    B_wrong = modexp(xB, a, q)

    print(f"Alice sends: {A_wrong}")
    print(f"Bob sends  : {B_wrong}")

    # They cannot compute a shared key
    print("❌ This method fails. No shared key can be computed.")


# --------------------------------------------------
# FIXED METHOD: Use x^a as NEW base, then do DH again
# --------------------------------------------------
def fixed_method(a, q, xA, xB):
    print("\n--- FIXED METHOD USING SECOND-STAGE DH ---")

    # First stage
    A1 = modexp(xA, a, q)
    B1 = modexp(xB, a, q)

    print(f"Alice sends first: {A1}")
    print(f"Bob sends first  : {B1}")

    # Second-stage DH
    keyA = modexp(B1, xA, q)
    keyB = modexp(A1, xB, q)

    print(f"Alice computes final key: {keyA}")
    print(f"Bob computes final key  : {keyB}")

    return keyA, keyB


# --------------------------------------------------
# Eve's capability test
# --------------------------------------------------
def eve_attack_test(a, q, xA, xB):
    print("\n--- EVE ATTACK TEST ---")

    # Eve sees only public data
    A1 = modexp(xA, a, q)
    B1 = modexp(xB, a, q)

    print(f"Eve sees A1 = {A1}")
    print(f"Eve sees B1 = {B1}")

    print("She must solve: find x from x^a mod q")
    print("This is as hard as discrete log → computationally infeasible.")
    print("❌ Eve cannot find Alice's or Bob's secret")
    print("❌ Eve cannot compute the shared key")


# --------------------------------------------------
# MAIN TEST
# --------------------------------------------------

# Public values
q = 353       # a small prime for demonstration
a = 3         # primitive root mod q

# Secret keys
xA = random.randint(2, q-2)
xB = random.randint(2, q-2)

print("Public q =", q)
print("Public a =", a)
print("Alice secret xA =", xA)
print("Bob secret xB =", xB)

# Run the three cases:
normal_dh(a, q, xA, xB)
wrong_method(a, q, xA, xB)
fixed_method(a, q, xA, xB)
eve_attack_test(a, q, xA, xB)
