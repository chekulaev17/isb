import sys
from const import ALPHABET, ALPHABET_SIZE

def get_key_letter(key: str, index: int) -> str:
    return key[index % len(key)]

def encrypt_letter(text_letter: str, key_letter: str) -> str:
    if text_letter in ALPHABET:
        text_index = ALPHABET.index(text_letter)
        key_index = ALPHABET.index(key_letter)
        return ALPHABET[(text_index + key_index) % ALPHABET_SIZE]
    return text_letter

def decrypt_letter(encrypted_letter: str, key_letter: str) -> str:
    if encrypted_letter in ALPHABET:
        enc_index = ALPHABET.index(encrypted_letter)
        key_index = ALPHABET.index(key_letter)
        return ALPHABET[(enc_index - key_index) % ALPHABET_SIZE]
    return encrypted_letter

def trithemius_encrypt(text: str, key: str) -> str:
    return "".join(encrypt_letter(text[i], get_key_letter(key, i)) for i in range(len(text)))

def trithemius_decrypt(encrypted_text: str, key: str) -> str:
    return "".join(decrypt_letter(encrypted_text[i], get_key_letter(key, i)) for i in range(len(encrypted_text)))

def read_file(filename: str) -> str:
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        sys.exit(1)

def write_file(filename: str, text: str) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)