import argparse
import json

from asymmetric import AsymmetricCrypto
from file_utils import FileUtils
from symmetric import SymmetricCrypto


def load_config(config_path='config.json') -> dict:
    """
    Load configuration from a JSON file.

    :param config_path: Path to the config JSON file
    :return: Configuration as a dictionary
    """
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Loading configuration failed: {str(e)}")


def generate_keys(config: dict):
    """
    Generate asymmetric keys and a symmetric key, then save them.

    :param config: Configuration dictionary
    """
    print("=== Key Generation Mode ===")
    try:
        key_settings = config['key_settings']
        sym_key = SymmetricCrypto.generate_key(config['aes_key_size'])
        private_key, public_key = AsymmetricCrypto.generate_keys()

        # Save asymmetric keys
        AsymmetricCrypto.save_public_key(public_key, key_settings['public_key'])
        AsymmetricCrypto.save_private_key(private_key, key_settings['private_key'])

        # Encrypt and save symmetric key
        encrypted_sym_key = AsymmetricCrypto.encrypt_with_public_key(sym_key, public_key)
        FileUtils.write_file(key_settings['encrypted_symmetric_key'], encrypted_sym_key)

        print("Keys successfully generated!")
    except Exception as e:
        print(f"Key generation failed: {str(e)}")


def encrypt_file(input_file: str, config: dict):
    """
    Encrypt a file using the configuration.

    :param input_file: Path to the input file
    :param config: Configuration dictionary
    """
    print("=== Encryption Mode ===")
    try:
        key_settings = config['key_settings']
        encryption_settings = config['encryption_settings']

        private_key = AsymmetricCrypto.load_private_key(key_settings['private_key'])
        encrypted_sym_key = FileUtils.read_file(key_settings['encrypted_symmetric_key'])
        sym_key = AsymmetricCrypto.decrypt_with_private_key(encrypted_sym_key, private_key)

        plaintext = FileUtils.read_file(input_file)
        ciphertext = SymmetricCrypto.encrypt(plaintext, sym_key)

        FileUtils.write_file(encryption_settings['default_encrypted'], ciphertext)
        print(f"File encrypted and saved as {encryption_settings['default_encrypted']}")
    except Exception as e:
        print(f"Encryption failed: {str(e)}")


def decrypt_file(input_file: str, config: dict):
    """
    Decrypt a file using the configuration.

    :param input_file: Path to the encrypted file
    :param config: Configuration dictionary
    """
    print("=== Decryption Mode ===")
    try:
        key_settings = config['key_settings']
        encryption_settings = config['encryption_settings']

        private_key = AsymmetricCrypto.load_private_key(key_settings['private_key'])
        encrypted_sym_key = FileUtils.read_file(key_settings['encrypted_symmetric_key'])
        sym_key = AsymmetricCrypto.decrypt_with_private_key(encrypted_sym_key, private_key)

        ciphertext = FileUtils.read_file(input_file)
        plaintext = SymmetricCrypto.decrypt(ciphertext, sym_key)

        FileUtils.write_file(encryption_settings['default_decrypted'], plaintext)
        print(f"File decrypted and saved as {encryption_settings['default_decrypted']}")
    except Exception as e:
        print(f"Decryption failed: {str(e)}")


def main():
    """
    Main entry point for the hybrid crypto system CLI.
    """
    try:
        config = load_config()

        parser = argparse.ArgumentParser(description="Hybrid Crypto System (AES + RSA)")
        subparsers = parser.add_subparsers(dest='command', required=True)

        # Parser for key generation
        subparsers.add_parser('gen', help='Generate keys')

        # Parser for encryption
        enc_parser = subparsers.add_parser('enc', help='Encrypt a file')
        enc_parser.add_argument('-i', '--input', help='Path to the file to encrypt',
                                default=config['encryption_settings']['default_input'])

        # Parser for decryption
        dec_parser = subparsers.add_parser('dec', help='Decrypt a file')
        dec_parser.add_argument('-i', '--input', help='Path to the encrypted file',
                                default=config['encryption_settings']['default_encrypted'])

        args = parser.parse_args()

        if args.command == 'gen':
            generate_keys(config)
        elif args.command == 'enc':
            encrypt_file(args.input, config)
        elif args.command == 'dec':
            decrypt_file(args.input, config)

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
