import random

def generate_substitution_key():
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    random.shuffle(alphabet)
    return {chr(65+i): alphabet[i] for i in range(26)}

def substitution_cipher(message, substitution_key):
    encrypted_message = ""
    for char in message:
        if char.isalpha():
            if char.isupper():
                encrypted_message += substitution_key[char]
            else:
                encrypted_message += substitution_key[char.upper()].lower()
        else:
            encrypted_message += char
    return encrypted_message

def substitution_decipher(encrypted_message, substitution_key):
    reversed_key = {v: k for k, v in substitution_key.items()}
    return substitution_cipher(encrypted_message, reversed_key)

# Exemple d'utilisation
message = "Bonjour, ceci est un message secret."
substitution_key = generate_substitution_key()
print("Clé de substitution:", substitution_key)

encrypted_message = substitution_cipher(message, substitution_key)
print("Message chiffré:", encrypted_message)

decrypted_message = substitution_decipher(encrypted_message, substitution_key)
print("Message déchiffré:", decrypted_message)
