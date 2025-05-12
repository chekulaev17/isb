import sys

from const import ALPHABET, ALPHABET_SIZE


def get_key_character(key: str, position: int) -> str:
    """
    Returns the corresponding character from the key at a specific position.
    :param key: The encryption key.
    :param position: The position in the text.
    :return: The character from the key at the given position.
    :raises ValueError: If the key is empty.
    """
    if not key:
        raise ValueError("The encryption key cannot be empty.")
    return key[position % len(key)]


def shift_character(char: str, key_char: str, encrypt: bool = True) -> str:
    """
    Encrypts or decrypts a single character using the modified Trithemius cipher.
    :param char: The character to encrypt/decrypt.
    :param key_char: The corresponding key character.
    :param encrypt: Whether to encrypt (True) or decrypt (False).
    :return: The transformed character.
    """
    try:
        text_index = ALPHABET.index(char.lower())
        key_index = ALPHABET.index(key_char.lower())
        new_index = (text_index + key_index) % ALPHABET_SIZE if encrypt else (text_index - key_index) % ALPHABET_SIZE
        return ALPHABET[new_index].upper() if char.isupper() else ALPHABET[new_index]
    except ValueError:
        return char


def process_text(text: str, key: str, encrypt: bool = True) -> str:
    """
    Encrypts or decrypts text using the modified Trithemius cipher.
    :param text: The input text.
    :param key: The encryption/decryption key.
    :param encrypt: Whether to encrypt (True) or decrypt (False).
    :return: The processed text.
    :raises ValueError: If the text or key is empty.
    """
    if not text:
        raise ValueError("The input text cannot be empty.")
    if not key:
        raise ValueError("The encryption key cannot be empty.")
    return "".join(shift_character(text[i], get_key_character(key, i), encrypt) for i in range(len(text)))


def read_file(file_path: str) -> str:
    """
    Reads the content of a file.
    :param file_path: The path to the file.
    :return: The file content as a string.
    :raises SystemExit: If the file is not found or cannot be read.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}", file=sys.stderr)
        sys.exit(1)


def write_file(file_path: str, content: str) -> None:
    """
    Writes content to a file.
    :param file_path: The path to the file.
    :param content: The text to be written.
    :raises SystemExit: If an error occurs while writing to the file.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Error writing to file '{file_path}': {e}", file=sys.stderr)
        sys.exit(1)
