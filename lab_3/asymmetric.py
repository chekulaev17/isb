from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding, rsa
from file_handler import FileHandler  # Добавлен импорт FileHandler


class AsymmetricCrypto:
    """
    Handles asymmetric (RSA) cryptographic operations.
    """

    @staticmethod
    def generate_keys():
        """
        Generate RSA private and public keys.

        :return: (private_key, public_key)
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        return private_key, private_key.public_key()

    @staticmethod
    def encrypt_with_public_key(data: bytes, public_key):
        """
        Encrypt data using the public RSA key.

        :param data: Data to encrypt.
        :param public_key: RSA public key.
        :return: Encrypted bytes.
        """
        return public_key.encrypt(
            data,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    @staticmethod
    def decrypt_with_private_key(encrypted_data: bytes, private_key):
        """
        Decrypt data using the private RSA key.

        :param encrypted_data: Encrypted data.
        :param private_key: RSA private key.
        :return: Decrypted bytes.
        """
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
        """
        Save private key to a file.

        :param private_key: RSA private key.
        :param file_path: Path to save the key.
        """
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        FileHandler.write_file(file_path, pem)

    @staticmethod
    def save_public_key(public_key, file_path: str):
        """
        Save public key to a file.

        :param public_key: RSA public key.
        :param file_path: Path to save the key.
        """
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        FileHandler.write_file(file_path, pem)

    @staticmethod
    def load_private_key(file_path: str):
        """
        Load private key from a file.

        :param file_path: Path to private key.
        :return: RSA private key.
        """
        return serialization.load_pem_private_key(
            FileHandler.read_file(file_path),
            password=None,
            backend=default_backend()
        )