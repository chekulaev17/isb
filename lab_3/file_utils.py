import os


class FileUtils:
    @staticmethod
    def read_file(file_path: str) -> bytes:
        """Чтение данных из файла"""
        with open(file_path, 'rb') as f:
            return f.read()

    @staticmethod
    def write_file(file_path: str, data: bytes):
        """Запись данных в файл"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(data)