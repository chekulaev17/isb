import os


class FileHandler:
    """
    Handles file operations.
    """

    @staticmethod
    def read_file(file_path: str) -> bytes:
        """
        Read binary data from a file.

        :param file_path: Path to file.
        :return: File content as bytes.
        """
        try:
            with open(file_path, 'rb') as f:
                return f.read()
        except Exception as e:
            raise RuntimeError(f"Failed to read file '{file_path}': {str(e)}")

    @staticmethod
    def write_file(file_path: str, data: bytes):
        """
        Write binary data to a file.

        :param file_path: Path to file.
        :param data: Data to write.
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(data)
        except Exception as e:
            raise RuntimeError(f"Failed to write file '{file_path}': {str(e)}")