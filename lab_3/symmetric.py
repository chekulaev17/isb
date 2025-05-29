import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class SymmetricCrypto:

    @staticmethod
    def encrypt(data: bytes, key: bytes) -> bytes:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padded_data = SymmetricCrypto._pad(data)
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return iv + encrypted_data

    @staticmethod
    def decrypt(encrypted_data: bytes, key: bytes) -> bytes:
        iv = encrypted_data[:16]
        actual_data = encrypted_data[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(actual_data) + decryptor.finalize()
        return SymmetricCrypto._unpad(padded_plaintext)

    @staticmethod
    def _pad(data: bytes) -> bytes:
        padder = padding.PKCS7(128).padder()
        return padder.update(data) + padder.finalize()

    @staticmethod
    def _unpad(padded_data: bytes) -> bytes:
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()


def encrypt_data(data: bytes, key: bytes) -> bytes:
    return SymmetricCrypto.encrypt(data, key)


def decrypt_data(encrypted_data: bytes, key: bytes) -> bytes:
    return SymmetricCrypto.decrypt(encrypted_data, key)
