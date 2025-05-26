from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

class SymmetricCrypto:

    def generate_key(key_size: int = 256) -> bytes:
        """Генерация симметричного ключа для AES"""
        if key_size not in [128, 192, 256]:
            raise ValueError("Неверный размер ключа. Допустимые значения: 128, 192, 256 бит")
        return os.urandom(key_size // 8)

    @staticmethod
    def pad_data(data: bytes) -> bytes:
        """Добавление padding к данным перед шифрованием"""
        padder = padding.PKCS7(128).padder()
        return padder.update(data) + padder.finalize()

    @staticmethod
    def unpad_data(padded_data: bytes) -> bytes:
        """Удаление padding после дешифрования"""
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()

    @staticmethod
    def encrypt(data: bytes, key: bytes) -> bytes:
        """Шифрование данных с использованием AES в режиме CBC"""
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padded_data = SymmetricCrypto.pad_data(data)
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return iv + encrypted_data

    @staticmethod
    def decrypt(encrypted_data: bytes, key: bytes) -> bytes:
        """Дешифрование данных с использованием AES"""
        iv = encrypted_data[:16]
        actual_data = encrypted_data[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(actual_data) + decryptor.finalize()
        return SymmetricCrypto.unpad_data(decrypted_padded)