import argparse
from symmetric import SymmetricCrypto
from asymmetric import AsymmetricCrypto
from file_utils import FileUtils


def generate_keys(encrypted_sym_key_path: str, public_key_path: str, private_key_path: str):
    """Генерация ключей гибридной системы"""
    print("=== Режим генерации ключей ===")

    # 1.1. Генерация симметричного ключа
    sym_key = SymmetricCrypto.generate_key(256)
    print("Симметричный ключ сгенерирован")

    # 1.2. Генерация асимметричных ключей
    private_key, public_key = AsymmetricCrypto.generate_keys()
    print("Асимметричные ключи сгенерированы")

    # 1.3. Сериализация асимметричных ключей
    AsymmetricCrypto.save_public_key(public_key, public_key_path)
    AsymmetricCrypto.save_private_key(private_key, private_key_path)
    print("Асимметричные ключи сохранены")

    # 1.4. Шифрование и сохранение симметричного ключа
    encrypted_sym_key = AsymmetricCrypto.encrypt_with_public_key(sym_key, public_key)
    FileUtils.write_file(encrypted_sym_key_path, encrypted_sym_key)
    print("Симметричный ключ зашифрован и сохранен")

    print("Все ключи успешно сгенерированы и сохранены!")


def encrypt_file(input_file: str, private_key_path: str,
                 encrypted_sym_key_path: str, output_file: str):
    """Шифрование файла гибридной системой"""
    print("=== Режим шифрования ===")

    # 2.1. Расшифровка симметричного ключа
    private_key = AsymmetricCrypto.load_private_key(private_key_path)
    encrypted_sym_key = FileUtils.read_file(encrypted_sym_key_path)
    sym_key = AsymmetricCrypto.decrypt_with_private_key(encrypted_sym_key, private_key)
    print("Симметричный ключ расшифрован")

    # 2.2. Шифрование файла
    plaintext = FileUtils.read_file(input_file)
    ciphertext = SymmetricCrypto.encrypt(plaintext, sym_key)
    FileUtils.write_file(output_file, ciphertext)
    print("Файл успешно зашифрован и сохранен")


def decrypt_file(input_file: str, private_key_path: str,
                 encrypted_sym_key_path: str, output_file: str):
    """Дешифрование файла гибридной системой"""
    print("=== Режим дешифрования ===")

    # 3.1. Расшифровка симметричного ключа
    private_key = AsymmetricCrypto.load_private_key(private_key_path)
    encrypted_sym_key = FileUtils.read_file(encrypted_sym_key_path)
    sym_key = AsymmetricCrypto.decrypt_with_private_key(encrypted_sym_key, private_key)
    print("Симметричный ключ расшифрован")

    # 3.2. Дешифрование файла
    ciphertext = FileUtils.read_file(input_file)
    plaintext = SymmetricCrypto.decrypt(ciphertext, sym_key)
    FileUtils.write_file(output_file, plaintext)
    print("Файл успешно расшифрован и сохранен")


def main():
    parser = argparse.ArgumentParser(description="Гибридная криптосистема (AES + RSA)")

    # Субпарсеры для разных режимов работы
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Парсер для генерации ключей
    gen_parser = subparsers.add_parser('gen', help='Генерация ключей')
    gen_parser.add_argument('encrypted_sym_key', help='Путь для сохранения зашифрованного симметричного ключа')
    gen_parser.add_argument('public_key', help='Путь для сохранения открытого ключа')
    gen_parser.add_argument('private_key', help='Путь для сохранения закрытого ключа')

    # Парсер для шифрования
    enc_parser = subparsers.add_parser('enc', help='Шифрование файла')
    enc_parser.add_argument('input_file', help='Путь к шифруемому файлу')
    enc_parser.add_argument('private_key', help='Путь к закрытому ключу')
    enc_parser.add_argument('encrypted_sym_key', help='Путь к зашифрованному симметричному ключу')
    enc_parser.add_argument('output_file', help='Путь для сохранения зашифрованного файла')

    # Парсер для дешифрования
    dec_parser = subparsers.add_parser('dec', help='Дешифрование файла')
    dec_parser.add_argument('input_file', help='Путь к зашифрованному файлу')
    dec_parser.add_argument('private_key', help='Путь к закрытому ключу')
    dec_parser.add_argument('encrypted_sym_key', help='Путь к зашифрованному симметричному ключу')
    dec_parser.add_argument('output_file', help='Путь для сохранения расшифрованного файла')

    args = parser.parse_args()

    if args.command == 'gen':
        generate_keys(args.encrypted_sym_key, args.public_key, args.private_key)
    elif args.command == 'enc':
        encrypt_file(args.input_file, args.private_key,
                     args.encrypted_sym_key, args.output_file)
    elif args.command == 'dec':
        decrypt_file(args.input_file, args.private_key,
                     args.encrypted_sym_key, args.output_file)


if __name__ == "__main__":
    main()