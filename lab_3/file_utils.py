import os


class FileUtils:


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
