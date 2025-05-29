import json
import os
from asymmetric import AsymmetricCrypto
from file_utils import read_file, write_file


def load_config(config_path='config.json') -> dict:
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Loading configuration failed: {str(e)}")


def generate_symmetric_key(key_size_bits: int) -> bytes:
    return os.urandom(key_size_bits // 8)


def handle_key_generation(config: dict):
    key_settings = config['key_settings']
    sym_key = generate_symmetric_key(config['aes_key_size'])
    private_key, public_key = AsymmetricCrypto.generate_keys()
    AsymmetricCrypto.save_public_key(public_key, key_settings['public_key'], write_file)
    AsymmetricCrypto.save_private_key(private_key, key_settings['private_key'], write_file)

    encrypted_sym_key = AsymmetricCrypto.encrypt_with_public_key(sym_key, public_key)
    write_file(key_settings['encrypted_symmetric_key'], encrypted_sym_key)
    print("Keys successfully generated!")


def get_symmetric_key(config: dict) -> bytes:
    key_settings = config['key_settings']
    private_key = AsymmetricCrypto.load_private_key(key_settings['private_key'], read_file)
    encrypted_sym_key = read_file(key_settings['encrypted_symmetric_key'])
    return AsymmetricCrypto.decrypt_with_private_key(encrypted_sym_key, private_key)
