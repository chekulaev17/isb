import sys
import argparse

from ciph import encrypt_text, decrypt_text, read_file, write_file


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
        if args.mode == 'encrypt':
            result_text = encrypt_text(input_text, key)
        else:
            result_text = decrypt_text(input_text, key)
        write_file(args.output_file, result_text)
        print(f"Operation '{args.mode}' completed successfully. Output saved to '{args.output_file}'.")

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
