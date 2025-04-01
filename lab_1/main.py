import argparse
from ciph import trithemius_encrypt, trithemius_decrypt, read_file, write_file

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["encrypt", "decrypt"], help="Choose mode: encrypt or decrypt")
    parser.add_argument("input_text", type=str, help="Input text file")
    parser.add_argument("output_text", type=str, help="Output text file")
    parser.add_argument("key_filename", type=str, help="File containing the encryption key")
    args = parser.parse_args()

    key = read_file(args.key_filename)
    input_text = read_file(args.input_text)
    result_text = trithemius_encrypt(input_text, key) if args.mode == "encrypt" else trithemius_decrypt(input_text, key)
    write_file(args.output_text, result_text)

if __name__ == "__main__":
    main()