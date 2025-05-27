import json
import argparse
from symmetric import SymmetricCrypto
from asymmetric import AsymmetricCrypto
from file_utils import FileUtils


def load_config(config_path='config.json'):
    """Загрузка конфигурации из JSON файла"""
    with open(config_path, 'r') as f:
        return json.load(f)


def generate_keys(config):
    """Генерация ключей с использованием параметров из конфига"""
    print("=== Режим генерации ключей ===")

    key_settings = config['key_settings']
    sym_key = SymmetricCrypto.generate_key(config['aes_key_size'])
    private_key, public_key = AsymmetricCrypto.generate_keys()

    # Сохранение ключей
    AsymmetricCrypto.save_public_key(public_key, key_settings['public_key'])
    AsymmetricCrypto.save_private_key(private_key, key_settings['private_key'])

    # Шифрование и сохранение симметричного ключа
    encrypted_sym_key = AsymmetricCrypto.encrypt_with_public_key(sym_key, public_key)
    FileUtils.write_file(key_settings['encrypted_symmetric_key'], encrypted_sym_key)

    print("Ключи успешно сгенерированы!")


def encrypt_file(input_file, config):
    """Шифрование файла с использованием конфига"""
    print("=== Режим шифрования ===")

    key_settings = config['key_settings']
    encryption_settings = config['encryption_settings']

    private_key = AsymmetricCrypto.load_private_key(key_settings['private_key'])
    encrypted_sym_key = FileUtils.read_file(key_settings['encrypted_symmetric_key'])
    sym_key = AsymmetricCrypto.decrypt_with_private_key(encrypted_sym_key, private_key)

    plaintext = FileUtils.read_file(input_file)
    ciphertext = SymmetricCrypto.encrypt(plaintext, sym_key)

    FileUtils.write_file(encryption_settings['default_encrypted'], ciphertext)
    print(f"Файл зашифрован и сохранен как {encryption_settings['default_encrypted']}")


def decrypt_file(input_file, config):
    """Дешифрование файла с использованием конфига"""
    print("=== Режим дешифрования ===")

    key_settings = config['key_settings']
    encryption_settings = config['encryption_settings']

    private_key = AsymmetricCrypto.load_private_key(key_settings['private_key'])
    encrypted_sym_key = FileUtils.read_file(key_settings['encrypted_symmetric_key'])
    sym_key = AsymmetricCrypto.decrypt_with_private_key(encrypted_sym_key, private_key)

    ciphertext = FileUtils.read_file(input_file)
    plaintext = SymmetricCrypto.decrypt(ciphertext, sym_key)

    FileUtils.write_file(encryption_settings['default_decrypted'], plaintext)
    print(f"Файл расшифрован и сохранен как {encryption_settings['default_decrypted']}")


def main():
    # Загрузка конфигурации
    config = load_config()

    parser = argparse.ArgumentParser(description="Гибридная криптосистема (AES + RSA)")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Парсер для генерации ключей
    subparsers.add_parser('gen', help='Генерация ключей')

    # Парсер для шифрования
    enc_parser = subparsers.add_parser('enc', help='Шифрование файла')
    enc_parser.add_argument('-i', '--input', help='Путь к файлу для шифрования',
                            default=config['encryption_settings']['default_input'])

    # Парсер для дешифрования
    dec_parser = subparsers.add_parser('dec', help='Дешифрование файла')
    dec_parser.add_argument('-i', '--input', help='Путь к зашифрованному файлу',
                            default=config['encryption_settings']['default_encrypted'])

    args = parser.parse_args()

    if args.command == 'gen':
        generate_keys(config)
    elif args.command == 'enc':
        encrypt_file(args.input, config)
    elif args.command == 'dec':
        decrypt_file(args.input, config)


if __name__ == "__main__":
    main()