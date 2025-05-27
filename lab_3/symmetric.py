import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class SymmetricCrypto:

    @staticmethod
    def generate_key(key_size: int = 256) -> bytes:
        """
        Generate a symmetric AES key.

        :param key_size: Key size in bits (128, 192, or 256)
        :return: Generated key as bytes
        """
        if key_size not in [128, 192, 256]:
            raise ValueError("Invalid key size. Allowed values: 128, 192, 256 bits")
        return os.urandom(key_size // 8)

    @staticmethod
    def pad_data(data: bytes) -> bytes:
        """
        Apply PKCS7 padding to data before encryption.

        :param data: Raw data as bytes
        :return: Padded data as bytes
        """
        padder = padding.PKCS7(128).padder()
        return padder.update(data) + padder.finalize()

    @staticmethod
    def unpad_data(padded_data: bytes) -> bytes:
        """
        Remove PKCS7 padding after decryption.

        :param padded_data: Padded data as bytes
        :return: Original unpadded data as bytes
        """
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()

    @staticmethod
    def encrypt(data: bytes, key: bytes) -> bytes:
        """
        Encrypt data using AES in CBC mode.

        :param data: Raw data as bytes
        :param key: AES key as bytes
        :return: IV + encrypted data as bytes
        """
        try:
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            padded_data = SymmetricCrypto.pad_data(data)
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
            return iv + encrypted_data
        except Exception as e:
            raise RuntimeError(f"Encryption failed: {str(e)}")

    @staticmethod
    def decrypt(encrypted_data: bytes, key: bytes) -> bytes:
        """
        Decrypt data using AES in CBC mode.

        :param encrypted_data: IV + encrypted data as bytes
        :param key: AES key as bytes
        :return: Decrypted original data as bytes
        """
        try:
            iv = encrypted_data[:16]
            actual_data = encrypted_data[16:]
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            decrypted_padded = decryptor.update(actual_data) + decryptor.finalize()
            return SymmetricCrypto.unpad_data(decrypted_padded)
        except Exception as e:
            raise RuntimeError(f"Decryption failed: {str(e)}")
