from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

def generate_key():
    return get_random_bytes(16)  # 16 bytes for AES-128, 24 bytes for AES-192, 32 bytes for AES-256

def encrypt(message, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv, ct

def decrypt(iv, ciphertext, key):
    iv_dec = base64.b64decode(iv)
    ct_dec = base64.b64decode(ciphertext)
    cipher = AES.new(key, AES.MODE_CBC, iv_dec)
    pt = unpad(cipher.decrypt(ct_dec), AES.block_size)
    return pt.decode('utf-8')

# Exemple d'utilisation
key = generate_key()
