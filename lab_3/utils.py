import json
import os
from asymmetric import AsymmetricCrypto
from file_handler import FileHandler


class CryptoUtils:
    """
    Utility functions for cryptographic operations.
    """

    @staticmethod
    def load_config(config_path='config.json') -> dict:
        """
        Load configuration from JSON file.

        :param config_path: Path to config.
        :return: Config dictionary.
        """
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise RuntimeError(f"Loading configuration failed: {str(e)}")

    @staticmethod
    def generate_symmetric_key(key_size_bits: int) -> bytes:
        """
        Generate a random symmetric AES key.

        :param key_size_bits: AES key size in bits.
        :return: Random key bytes.
        """
        return os.urandom(key_size_bits // 8)

    @staticmethod
    def handle_key_generation(config: dict):
        """
        Handle the generation of RSA keys and symmetric key, and store them.

        :param config: Configuration dictionary.
        """
        try:
            key_settings = config['key_settings']
            sym_key = CryptoUtils.generate_symmetric_key(config['aes_key_size'])
            private_key, public_key = AsymmetricCrypto.generate_keys()

            AsymmetricCrypto.save_public_key(public_key, key_settings['public_key'])
            AsymmetricCrypto.save_private_key(private_key, key_settings['private_key'])

            encrypted_sym_key = AsymmetricCrypto.encrypt_with_public_key(sym_key, public_key)
            FileHandler.write_file(key_settings['encrypted_symmetric_key'], encrypted_sym_key)
            print("Keys successfully generated!")
        except Exception as e:
            raise RuntimeError(f"Key generation failed: {str(e)}")

    @staticmethod
    def get_symmetric_key(config: dict) -> bytes:
        """
        Retrieve the decrypted symmetric key.

        :param config: Configuration dictionary.
        :return: Symmetric AES key.
        """
        try:
            key_settings = config['key_settings']
            private_key = AsymmetricCrypto.load_private_key(key_settings['private_key'])
            encrypted_sym_key = FileHandler.read_file(key_settings['encrypted_symmetric_key'])
            return AsymmetricCrypto.decrypt_with_private_key(encrypted_sym_key, private_key)
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve symmetric key: {str(e)}")