import random

def generate_substitution_key():
    alphabet = [i for i in range(256)]
    random.shuffle(alphabet)
    return {i: alphabet[i] for i in range(256)}
