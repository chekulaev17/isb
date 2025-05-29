from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding, rsa


class AsymmetricCrypto:

    @staticmethod
    def generate_keys():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def encrypt_with_public_key(data: bytes, public_key) -> bytes:
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
        return private_key.decrypt(
            encrypted_data,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    @staticmethod
    def save_private_key(private_key, file_path: str, write_func):
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        write_func(file_path, pem)

    @staticmethod
    def save_public_key(public_key, file_path: str, write_func):
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        write_func(file_path, pem)

    @staticmethod
    def load_private_key(file_path: str, read_func):
        return serialization.load_pem_private_key(
            read_func(file_path),
            password=None,
            backend=default_backend()
        )

    @staticmethod
    def load_public_key(file_path: str, read_func):
        return serialization.load_pem_public_key(
            read_func(file_path),
            backend=default_backend()
        )
