import argparse
from utils import load_config, handle_key_generation, get_symmetric_key
from file_utils import read_file, write_file
from symmetric import encrypt_data, decrypt_data


def main():
    config = load_config()

    parser = argparse.ArgumentParser(description="Hybrid Crypto System (AES + RSA)")
    subparsers = parser.add_subparsers(dest='command', required=True)

    subparsers.add_parser('gen', help='Generate keys')

    enc_parser = subparsers.add_parser('enc', help='Encrypt a file')
    enc_parser.add_argument('-i', '--input', help='Path to the file to encrypt',
                            default=config['encryption_settings']['default_input'])

    dec_parser = subparsers.add_parser('dec', help='Decrypt a file')
    dec_parser.add_argument('-i', '--input', help='Path to the encrypted file',
                            default=config['encryption_settings']['default_encrypted'])

    args = parser.parse_args()

    if args.command == 'gen':
        handle_key_generation(config)
    elif args.command == 'enc':
        sym_key = get_symmetric_key(config)
        plaintext = read_file(args.input)
        ciphertext = encrypt_data(plaintext, sym_key)
        write_file(config['encryption_settings']['default_encrypted'], ciphertext)
        print(f"File encrypted and saved as {config['encryption_settings']['default_encrypted']}")
    elif args.command == 'dec':
        sym_key = get_symmetric_key(config)
        ciphertext = read_file(args.input)
        plaintext = decrypt_data(ciphertext, sym_key)
        write_file(config['encryption_settings']['default_decrypted'], plaintext)
        print(f"File decrypted and saved as {config['encryption_settings']['default_decrypted']}")


if __name__ == "__main__":
    main()
