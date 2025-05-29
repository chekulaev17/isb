import os


def read_file(file_path: str) -> bytes:
    with open(file_path, 'rb') as f:
        return f.read()


def write_file(file_path: str, data: bytes):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as f:
        f.write(data)
