import sys

from const import ALPHABET, ALPHABET_SIZE


def get_key_symb(key: str, index: int) -> str:
    """
    Retrieves the corresponding character from the repeating key sequence.
    :param key: The encryption key.
    :param index: The index of the character in the text.
    :return: The corresponding character from the key.
    :raises ValueError: If the key is empty.
    """
    if not key:
        raise ValueError("The key cannot be empty.")
    return key[index % len(key)]


def get_encrypted_symb(old_sym: str, key_sym: str) -> str:
    """
    Encrypts a single character using the Trithemius cipher.
    :param old_sym: The original character.
    :param key_sym: The corresponding key character.
    :return: The encrypted character.
    """
    try:
        current_idx = ALPHABET.index(old_sym.lower())
        key_idx = ALPHABET.index(key_sym.lower())
        encrypt_idx = (current_idx + key_idx) % ALPHABET_SIZE
        return ALPHABET[encrypt_idx].upper() if old_sym.isupper() else ALPHABET[encrypt_idx]
    except ValueError:
        return old_sym  # Non-alphabetic characters remain unchanged.


def get_decrypted_symb(encrypted_sym: str, key_sym: str) -> str:
    """
    Decrypts a single character using the Trithemius cipher.
    :param encrypted_sym: The encrypted character.
    :param key_sym: The corresponding key character.
    :return: The decrypted character.
    """
    try:
        encrypted_idx = ALPHABET.index(encrypted_sym.lower())
        key_idx = ALPHABET.index(key_sym.lower())
        decrypted_idx = (encrypted_idx - key_idx) % ALPHABET_SIZE
        return ALPHABET[decrypted_idx].upper() if encrypted_sym.isupper() else ALPHABET[decrypted_idx]
    except ValueError:
        return encrypted_sym  # Non-alphabetic characters remain unchanged.


def vigenere_cipher_encrypt(input_text: str, key: str) -> str:
    """
    Encrypts text using the Trithemius cipher.
    :param input_text: The plaintext to be encrypted.
    :param key: The encryption key.
    :return: The encrypted text.
    :raises ValueError: If the input text or key is empty.
    """
    if not input_text:
        raise ValueError("Input text cannot be empty.")

    if not key:
        raise ValueError("Key cannot be empty.")
    return "".join(get_encrypted_symb(input_text[i], get_key_symb(key, i)) for i in range(len(input_text)))


def vigenere_cipher_decrypt(encrypted_text: str, key: str) -> str:
    """
    Decrypts text encrypted with the Trithemius cipher.
    :param encrypted_text: The encrypted text.
    :param key: The decryption key.
    :return: The decrypted text.
    :raises ValueError: If the encrypted text or key is empty.
    """
    if not encrypted_text:
        raise ValueError("Encrypted text cannot be empty.")

    if not key:
        raise ValueError("Key cannot be empty.")
        return "".join(get_decrypted_symb(encrypted_text[i], get_key_symb(key, i)) for i in range(len(encrypted_text)))


def read_text(filename: str) -> str:
        """
        Reads text from a file.
        :param filename: The path to the input file.
        :return: The file content as a string.
        :raises SystemExit: If the file is not found or another error occurs.
        """
        try:
            with open(filename, 'r', encoding='utf-8') as text:
                return text.read().strip()

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file '{filename}': {e}", file=sys.stderr)
            sys.exit(1)


def write_text(filename: str, text: str) -> None:
        """
        Writes text to a file.
        :param filename: The path to the output file.
        :param text: The text to write.
        :raises SystemExit: If an error occurs while writing to the file.
        """
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(text)

        except Exception as e:
            print(f"Error writing to file '{filename}': {e}", file=sys.stderr)
            sys.exit(1)