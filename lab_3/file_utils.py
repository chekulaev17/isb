import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


class FileUtils:

    @staticmethod
    def read_file(file_path: str) -> bytes:
        """
        Read data from a file.

        :param file_path: Path to the file
        :return: File content as bytes
        """
        try:
            with open(file_path, 'rb') as f:
                return f.read()
        except Exception as e:
            raise RuntimeError(f"Reading file failed: {str(e)}")

    @staticmethod
    def write_file(file_path: str, data: bytes):
        """
        Write data to a file.

        :param file_path: Destination file path
        :param data: Data to write as bytes
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(data)
        except Exception as e:
            raise RuntimeError(f"Writing file failed: {str(e)}")

    @staticmethod
    def save_private_key_to_file(private_key, file_path: str):
        """
        Save the private key to a file.

        :param private_key: RSA private key object
        :param file_path: Destination file path
        """
        try:
            pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            FileUtils.write_file(file_path, pem)
        except Exception as e:
            raise RuntimeError(f"Saving private key to file failed: {str(e)}")

    @staticmethod
    def save_public_key_to_file(public_key, file_path: str):
        """
        Save the public key to a file.

        :param public_key: RSA public key object
        :param file_path: Destination file path
        """
        try:
            pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            FileUtils.write_file(file_path, pem)
        except Exception as e:
            raise RuntimeError(f"Saving public key to file failed: {str(e)}")

    @staticmethod
    def load_private_key_from_file(file_path: str):
        """
        Load the private key from a file.

        :param file_path: Path to the private key file
        :return: RSA private key object
        """
        try:
            data = FileUtils.read_file(file_path)
            return serialization.load_pem_private_key(
                data,
                password=None,
                backend=default_backend()
            )
        except Exception as e:
            raise RuntimeError(f"Loading private key from file failed: {str(e)}")

    @staticmethod
    def load_public_key_from_file(file_path: str):
        """
        Load the public key from a file.

        :param file_path: Path to the public key file
        :return: RSA public key object
        """
        try:
            data = FileUtils.read_file(file_path)
            return serialization.load_pem_public_key(
                data,
                backend=default_backend()
            )
        except Exception as e:
            raise RuntimeError(f"Loading public key from file failed: {str(e)}")
