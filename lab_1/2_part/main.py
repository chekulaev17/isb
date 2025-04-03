import json
import sys

from collections import OrderedDict, Counter
from constants import RUSSIAN_FREQ
from config import ENCRYPTED_FILE, DECRYPTED_FILE, KEY_FILE


def save_to_json(filename: str, data: dict) -> None:
    """
    Saves a dictionary to a JSON file.
    :param filename: The name of the file.
    :param data: The dictionary to save.
    :return: None
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving to file '{filename}': {e}")
        raise


def save_to_text(filename: str, text: str) -> None:
    """
    Saves text to a file.
    :param filename: The name of the file.
    :param text: The text to save.
    :return: None
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
    except Exception as e:
        print(f"Error writing to file '{filename}': {e}")
        raise


def load_from_json(filename: str) -> dict:
    """
    Loads a dictionary from a JSON file.
    :param filename: The name of the file.
    :return: The loaded dictionary.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        raise
    except json.JSONDecodeError:
        print(f"JSON decoding error in file '{filename}'.")
        raise


def calculate_frequency(text: str) -> dict:
    """
    Calculates and sorts the frequency of characters in a text.
    :param text: The input text.
    :return: An ordered dictionary mapping characters to their frequency, sorted in descending order.
    """
    if not text:
        raise ValueError("Input text cannot be empty.")
    counter = Counter(text)
    total_chars = len(text)
    freq_dict = {char: round(count / total_chars, 6) for char, count in counter.items()}
    return OrderedDict(sorted(freq_dict.items(), key=lambda x: x[1], reverse=True))


def create_decryption_key(encrypted_freq: dict, reference_freq: dict) -> dict:
    """
    Creates a mapping between encrypted and reference characters based on frequency analysis.
    :param encrypted_freq: The character frequencies in the encrypted text.
    :param reference_freq: The character frequencies in the reference text.
    :return: A dictionary mapping encrypted characters to reference characters.
    """
    if not encrypted_freq or not reference_freq:
        raise ValueError("Both frequency dictionaries must be non-empty.")
    return {enc: rus for (enc, _), (rus, _) in zip(encrypted_freq.items(), reference_freq.items())}


def decrypt_text(encrypted_text: str, key: dict) -> str:
    """
    Decrypts text using a character mapping.
    :param encrypted_text: The encrypted text.
    :param key: The dictionary mapping encrypted characters to decrypted characters.
    :return: The decrypted text.
    """
    if not encrypted_text:
        raise ValueError("Encrypted text cannot be empty.")
    if not key:
        raise ValueError("Decryption key cannot be empty.")
    return ''.join(key.get(char, char) for char in encrypted_text)


def main() -> None:
    """
    Main function to handle the encryption analysis and decryption process.
    Reads the encrypted text, calculates frequencies, creates a decryption key, and outputs the decrypted text.
    """
    try:
        with open(ENCRYPTED_FILE, 'r', encoding='utf-8') as file:
            encrypted_text = file.read()
    except FileNotFoundError:
        print(f"Error: File '{ENCRYPTED_FILE}' not found!")
        sys.exit(1)
    if not encrypted_text.strip():
        print("Error: Encrypted text is empty!")
        sys.exit(1)
    try:
        sorted_encrypted_freq = calculate_frequency(encrypted_text)
        sorted_russian_freq = OrderedDict(sorted(RUSSIAN_FREQ.items(), key=lambda x: x[1], reverse=True))
        decryption_key = create_decryption_key(sorted_encrypted_freq, sorted_russian_freq)
        decrypted_text = decrypt_text(encrypted_text, decryption_key)
    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error during decryption: {e}")
        sys.exit(1)
    try:
        save_to_json(KEY_FILE, decryption_key)
        save_to_text(DECRYPTED_FILE, decrypted_text)
    except Exception as e:
        print(f"Error during saving files: {e}")
        sys.exit(1)
    print("Original text (first 1000 characters of encrypted text):")
    print(encrypted_text[:1000])
    print("\nDecrypted text (first 1000 characters):")
    print(decrypted_text[:1000])
    print("\nCharacter mapping key:")
    print(json.dumps(decryption_key, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
