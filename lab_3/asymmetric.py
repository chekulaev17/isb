from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding, rsa


class AsymmetricCrypto:

    @staticmethod
    def generate_keys() -> tuple:
        """
        Generate an RSA private-public key pair.

        :return: Tuple (private_key, public_key)
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def encrypt_with_public_key(data: bytes, public_key) -> bytes:
        """
        Encrypt data using an RSA public key.

        :param data: Data to encrypt as bytes
        :param public_key: RSA public key object
        :return: Encrypted data as bytes
        """
        try:
            return public_key.encrypt(
                data,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        except Exception as e:
            raise RuntimeError(f"Encryption with public key failed: {str(e)}")

    @staticmethod
    def decrypt_with_private_key(encrypted_data: bytes, private_key) -> bytes:
        """
        Decrypt data using an RSA private key.

        :param encrypted_data: Encrypted data as bytes
        :param private_key: RSA private key object
        :return: Decrypted original data as bytes
        """
        try:
            return private_key.decrypt(
                encrypted_data,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        except Exception as e:
            raise RuntimeError(f"Decryption with private key failed: {str(e)}")
