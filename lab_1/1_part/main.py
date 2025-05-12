import argparse
import sys

from const import ALPHABET, ALPHABET_SIZE
from ciph import process_text, read_file, write_file


def create_parser():
    """
    Creates and configures the argument parser for the CLI.
    :return: Configured argument parser.
    """
    parser = argparse.ArgumentParser(description="Encrypt or decrypt text using the Trithemius cipher.")
    parser.add_argument('mode', choices=['encrypt', 'decrypt'], help="Operation mode: 'encrypt' or 'decrypt'.")
    parser.add_argument('input_file', type=str, help="Path to the input text file.")
    parser.add_argument('output_file', type=str, help="Path to the output text file.")
    parser.add_argument('key_file', type=str, help="Path to the file containing the encryption key.")
    return parser


def main():
    """
    Main function that processes user input and performs encryption or decryption.
    :raises SystemExit: If an error occurs during processing.
    """
    parser = create_parser()
    args = parser.parse_args()
    try:
        key = read_file(args.key_file)
        input_text = read_file(args.input_file)

        if not key:
            raise ValueError("The encryption key cannot be empty.")
        if not input_text:
            raise ValueError("The input text cannot be empty.")

        result_text = process_text(input_text, key, encrypt=(args.mode == 'encrypt'))
        write_file(args.output_file, result_text)
        print(f"Operation '{args.mode}' completed successfully. Output saved to '{args.output_file}'.")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"File error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
