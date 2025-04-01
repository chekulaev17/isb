import argparse
import sys

from ciph import vigenere_cipher_encrypt, vigenere_cipher_decrypt, read_text, write_text


def parser_create():
    """
    Creates a command-line argument parser.
    :return: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Encrypt or decrypt text using the Trithemius cipher.")
    parser.add_argument('mode', choices=['encrypt', 'decrypt'], help="Mode: 'encrypt' to encrypt, 'decrypt' to decrypt.")
    parser.add_argument('input_text', type=str, help="Path to the input text file.")
    parser.add_argument('output_text', type=str, help="Path to the output text file.")
    parser.add_argument('key_filename', type=str, help="Path to the file containing the encryption key.")
    return parser.parse_args()


def main():
    """
    Main function that processes user input and executes encryption or decryption.
    :raises SystemExit: If an error occurs during processing.
    """
    args = parser_create()
    key = read_text(args.key_filename)
    input_text = read_text(args.input_text)
    try:
        if args.mode == 'encrypt':
            result_text = vigenere_cipher_encrypt(input_text, key)
        else:
            result_text = vigenere_cipher_decrypt(input_text, key)
        write_text(args.output_text, result_text)
        print(f"Result saved to {args.output_text}")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()