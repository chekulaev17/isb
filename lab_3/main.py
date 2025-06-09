import argparse
from utils import CryptoUtils
from file_handler import FileHandler
from symmetric import SymmetricCrypto


def main():
    """
    Main entry point: parse CLI arguments and run appropriate mode.
    """
    try:
        config = CryptoUtils.load_config()

        parser = argparse.ArgumentParser(description="Hybrid Crypto System (AES + RSA)")
        subparsers = parser.add_subparsers(dest='command', required=True)

        subparsers.add_parser('gen', help='Generate keys')

        enc_parser = subparsers.add_parser('enc', help='Encrypt a file')
        enc_parser.add_argument('-i', '--input',
                              help='Path to the file to encrypt',
                              default=config['encryption_settings']['default_input'])

        dec_parser = subparsers.add_parser('dec', help='Decrypt a file')
        dec_parser.add_argument('-i', '--input',
                               help='Path to the encrypted file',
                               default=config['encryption_settings']['default_encrypted'])

        args = parser.parse_args()

        if args.command == 'gen':
            CryptoUtils.handle_key_generation(config)
            print("Keys successfully generated!")
        elif args.command == 'enc':
            sym_key = CryptoUtils.get_symmetric_key(config)
            plaintext = FileHandler.read_file(args.input)
            ciphertext = SymmetricCrypto.encrypt(plaintext, sym_key)
            FileHandler.write_file(config['encryption_settings']['default_encrypted'], ciphertext)
            print(f"File encrypted and saved as {config['encryption_settings']['default_encrypted']}")
        elif args.command == 'dec':
            sym_key = CryptoUtils.get_symmetric_key(config)
            ciphertext = FileHandler.read_file(args.input)
            plaintext = SymmetricCrypto.decrypt(ciphertext, sym_key)
            FileHandler.write_file(config['encryption_settings']['default_decrypted'], plaintext)
            print(f"File decrypted and saved as {config['encryption_settings']['default_decrypted']}")

    except Exception as e:
        print(f"[ERROR] {str(e)}")


if __name__ == "__main__":
    main()