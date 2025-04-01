import json

from collections import OrderedDict, Counter

def save_to_json(filename: str, data: dict) -> None:
    """Сохраняет словарь в JSON-файл."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка при сохранении в файл '{filename}': {e}")
        raise

def load_from_json(filename: str) -> dict:
    """Загружает словарь из JSON-файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден.")
        raise
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON в файле '{filename}'.")
        raise

def calculate_frequency(text: str) -> dict:
    """Подсчитывает частоту символов в тексте."""
    if not text:
        raise ValueError("Входной текст не может быть пустым.")
    counter = Counter(text)
    total_chars = len(text)
    return {char: round(count / total_chars, 6) for char, count in counter.items()}

def sort_frequencies(freq_dict: dict) -> dict:
    """Сортирует частоты символов по убыванию."""
    return OrderedDict(sorted(freq_dict.items(), key=lambda x: x[1], reverse=True))

def create_decryption_key(encrypted_freq: dict, reference_freq: dict) -> dict:
    """Создаёт словарь соответствий между зашифрованными и русскими символами."""
    if not encrypted_freq or not reference_freq:
        raise ValueError("Оба словаря частот должны быть не пустыми.")
    return {enc: rus for (enc, _), (rus, _) in zip(encrypted_freq.items(), reference_freq.items())}

def decrypt_text(encrypted_text: str, key: dict) -> str:
    """Дешифрует текст, используя словарь замен."""
    if not encrypted_text:
        raise ValueError("Зашифрованный текст не может быть пустым.")
    if not key:
        raise ValueError("Словарь соответствий не может быть пустым.")
    return ''.join(key.get(char, char) for char in encrypted_text)

def main():
    import sys
    from constants import RUSSIAN_FREQ

    try:
        with open('cod19.txt', 'r', encoding='utf-8') as file:
            encrypted_text = file.read()
    except FileNotFoundError:
        print("Ошибка: Файл 'cod19.txt' не найден!")
        sys.exit(1)

    if not encrypted_text.strip():
        print("Ошибка: Зашифрованный текст пуст!")
        sys.exit(1)

    encrypted_freq = calculate_frequency(encrypted_text)
    sorted_encrypted_freq = sort_frequencies(encrypted_freq)
    sorted_russian_freq = sort_frequencies(RUSSIAN_FREQ)
    decryption_key = create_decryption_key(sorted_encrypted_freq, sorted_russian_freq)
    decrypted_text = decrypt_text(encrypted_text, decryption_key)

    save_to_json('key.json', decryption_key)

    try:
        with open('decrypted_text.txt', 'w', encoding='utf-8') as file:
            file.write(decrypted_text)
    except Exception as e:
        print(f"Ошибка при записи в файл 'decrypted_text.txt': {e}")

    print("Исходный текст (первые 1000 символов зашифрованного текста):")
    print(encrypted_text[:1000])
    print("\nДешифрованный текст (первые 1000 символов):")
    print(decrypted_text[:1000])
    print("\nКлюч соответствий символов:")
    print(decryption_key)


if __name__ == "__main__":
    main()

