import random
import sympy

def generate_keypair(bits):
    p = sympy.randprime(2**(bits//2), 2**(bits//2 + 1))
    q = sympy.randprime(2**(bits//2), 2**(bits//2 + 1))
    n = p * q
    g = n + 1
    lcm = sympy.lcm(p - 1, q - 1)
    mu = sympy.mod_inverse(lcm, n)
    public_key = (n, g)
    private_key = (int(lcm), int(mu))
    return public_key, private_key

def encrypt(public_key, plaintext):
    n, g = public_key
    r = random.randint(1, n - 1)
    n_squared = n * n
    ciphertext = (pow(g, plaintext, n_squared) * pow(r, n, n_squared)) % n_squared
    return ciphertext

def decrypt(public_key, private_key, ciphertext):
    n, _ = public_key
    lambda_val, mu = private_key
    n_squared = n * n
    lambda_val = int(lambda_val)  # Convertir lambda_val en int
    plaintext = ((pow(ciphertext, lambda_val, n_squared) - 1) // n) * mu % n
    return plaintext

# Exemple d'utilisation :
# public_key, private_key = generate_keypair(16)
# plaintext = 50
# ciphertext = encrypt(public_key, plaintext)
# decrypted_plaintext = decrypt(public_key, private_key, ciphertext)
# print("Plaintext:", plaintext)
# print("Ciphertext:", ciphertext)
# print("Decrypted Plaintext:", decrypted_plaintext)
