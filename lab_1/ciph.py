from const import ALPHABET, ALPHABET_SIZE

def get_key_letter(key: str, index: int) -> str:
    return key[index % len(key)]

def encrypt_letter(text_letter: str, key_letter: str) -> str:
    if text_letter in ALPHABET:
        text_index = ALPHABET.index(text_letter)
        key_index = ALPHABET.index(key_letter)
        return ALPHABET[(text_index + key_index) % ALPHABET_SIZE]
    return text_letter
