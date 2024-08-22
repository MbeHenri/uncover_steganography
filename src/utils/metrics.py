def string_to_binary(string):
    binary_string = "".join(format(ord(char), "08b") for char in string)
    return binary_string


def BER(original_string, received_string):
    if len(original_string) != len(received_string):
        raise ValueError("Les séquences de caractères doivent avoir la même longueur.")

    original_bits = string_to_binary(original_string)
    received_bits = string_to_binary(received_string)

    total_bits = len(original_bits)
    # print(total_bits)
    error_count = sum(
        original_bit != received_bit
        for original_bit, received_bit in zip(original_bits, received_bits)
    )
    ber = error_count / total_bits
    return ber


def ER(original_string, received_string):
    if len(original_string) != len(received_string):
        raise ValueError("Les séquences de caractères doivent avoir la même longueur.")

    return sum([1 if e != "_" else 0 for e in received_string]) / len(original_string)
