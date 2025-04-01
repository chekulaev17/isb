import json
from collections import OrderedDict
from constants import RUSSIAN_FREQ  # Подключаем частоты русского алфавита
import os  # Для проверки существования файлов

# Частоты символов из зашифрованного текста
ENCRYPTED_FREQ = {
    'Y': 0.099256, '8': 0.01861, 'S': 0.059553, '-': 0.074442, 't': 0.029777, 'A': 0.119107,
    '!': 0.016129, 'Q': 0.039702, 'x': 0.038462, '3': 0.021092, 'd': 0.014888, 'G': 0.022333,
    'R': 0.016129, 'J': 0.07072, '=': 0.011166, 'U': 0.009926, 'I': 0.039702, 'L': 0.062035,
    'K': 0.027295, 'O': 0.032258, '$': 0.07072, 'Z': 0.011166, 'F': 0.016129, 'E': 0.004963,
    'n': 0.011166, 'C': 0.007444, 'B': 0.007444, '\n': 0.011166, 'h': 0.012407, 'W': 0.012407,
    'M': 0.003722, '>': 0.004963, ' ': 0.002481, '9': 0.001241
}

# 1. Сортируем символы по убыванию частоты
sorted_encrypted_freq = OrderedDict(sorted(ENCRYPTED_FREQ.items(), key=lambda x: x[1], reverse=True))
sorted_russian_freq = OrderedDict(sorted(RUSSIAN_FREQ.items(), key=lambda x: x[1], reverse=True))

# 2. Создаём словарь соответствия (замены символов)
decryption_key = {}
for (enc_char, _), (rus_char, _) in zip(sorted_encrypted_freq.items(), sorted_russian_freq.items()):
    decryption_key[enc_char] = rus_char

# 3. Функция дешифровки текста
def decrypt_text(encrypted_text: str, key: dict) -> str:
    """
    Расшифровывает текст, заменяя символы по частотному анализу.
    :param encrypted_text: зашифрованный текст.
    :param key: словарь соответствий символов.
    :return: расшифрованный текст.
    """
    return ''.join([key.get(char, char) for char in encrypted_text])

# 4. Чтение зашифрованного текста (читаем файл cod19.txt)
with open('cod19.txt', 'r', encoding='utf-8') as file:
    encrypted_text = file.read()

# 5. Дешифруем текст
decrypted_text = decrypt_text(encrypted_text, decryption_key)

# 6. Проверяем и создаем файлы для дешифрованного текста и ключа
decrypted_text_path = 'decrypted_text.txt'
key_path = 'key.json'

# Если файл с дешифрованным текстом не существует, создаем его
if not os.path.exists(decrypted_text_path):
    with open(decrypted_text_path, 'w', encoding='utf-8') as file:
        file.write(decrypted_text)

# Если файл с ключом не существует, создаем его
if not os.path.exists(key_path):
    with open(key_path, 'w', encoding='utf-8') as file:
        json.dump(decryption_key, file, ensure_ascii=False, indent=4)

# 7. Выводим результат
print("Исходный текст (зашифрованный):")
print(encrypted_text[:500])  # Выводим первые 500 символов
print("\nДешифрованный текст:")
print(decrypted_text[:500])  # Выводим первые 500 символов
print("\nНайденный ключ соответствий символов:")
print(decryption_key)
