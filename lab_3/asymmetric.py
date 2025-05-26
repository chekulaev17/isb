from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class AsymmetricCrypto:
    @staticmethod
    def generate_keys() -> tuple:
        """Генерация пары RSA ключей"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def encrypt_with_public_key(data: bytes, public_key) -> bytes:
        """Шифрование данных с использованием публичного ключа RSA"""
        return public_key.encrypt(
            data,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    @staticmethod
    def decrypt_with_private_key(encrypted_data: bytes, private_key) -> bytes:
        """Дешифрование данных с использованием приватного ключа RSA"""
        return private_key.decrypt(
            encrypted_data,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    @staticmethod
    def save_private_key(private_key, file_path: str):
        """Сохранение приватного ключа в файл"""
        with open(file_path, 'wb') as f:
            f.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )

    @staticmethod
    def save_public_key(public_key, file_path: str):
        """Сохранение публичного ключа в файл"""
        with open(file_path, 'wb') as f:
            f.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )

    @staticmethod
    def load_private_key(file_path: str):
        """Загрузка приватного ключа из файла"""
        with open(file_path, 'rb') as f:
            return serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )

    @staticmethod
    def load_public_key(file_path: str):
        """Загрузка публичного ключа из файла"""
        with open(file_path, 'rb') as f:
            return serialization.load_pem_public_key(
                f.read(),
                backend=default_backend()
            )