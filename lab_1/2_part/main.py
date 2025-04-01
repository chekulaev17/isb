import json

def calculate_frequency(text: str) -> dict:
    """
    Подсчитывает частоту каждого символа в тексте.
    :param text: Входной текст.
    :return: Словарь с символами и их частотой.
    """
    freq = {}
    total_symbols = len(text)

    # Подсчёт количества каждого символа
    for char in text:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1

    # Преобразуем количество символов в частоту
    for char in freq:
        freq[char] = round(freq[char] / total_symbols, 6)

    return freq

def save_frequency_to_json(filename: str, freq_dict: dict) -> None:
    """
    Сохраняет словарь частот в JSON файл.
    :param filename: Имя файла для сохранения.
    :param freq_dict: Словарь с частотами символов.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(freq_dict, f, ensure_ascii=False)

def load_frequency_from_json(filename: str) -> dict:
    """
    Загружает словарь частот из JSON файла.
    :param filename: Имя файла для загрузки.
    :return: Словарь с частотами символов.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


# Пример зашифрованного текста (в вашем случае замените это на ваш текст)
encrypted_text = '''Y8S-tA-!AYQSYxS3dAGYSRJ-=A-SUYItLJ-K-ARxOR$JQRALOZYIJtAJYA$QJFAGYQO$8YxLJ$OFSYQJFA8$=QJx-=A8ORAI$E$SRA!L8LnCUU$KJ-xS3$ALOZYI-Jt3AGYtYZLBJAYGJ-t-!-IYxLJFAILhYJWAGIYZILttA-AQQJ$tAnJYAYQYh$SSYALKJWLOFSYAxACGYdWAhYOFEdA8LSS3d
GIYZILtt-IYxLS-$AxAQxYBAYn$I$8FAGY!xYOR$JAQY!8LxLJFAGI-OYM$S-RAAQ-QJ$t3AKYJYI3$ALxJYtLJ-!-IWBJAIWJ-SS3$A!L8Ln-AYh$QG$nxLRAW8YhQJxYA-AQKYIYQJFAx3GYOS$S-RAYG$IL>-=QAIL!x-J-$tAJ$dSYOYZ-=AJLK-dAKLKA-QKWQQJx$SS3=ASJ$OO$KJA-AtLE-SSY$AYhWn$S-$A-SUYItLJ-KLAQJLSYxJQRA$9$AhYO$$AxLMSY=
CJ-ASLGILxO$S-RAYJKI3xLBJASYx3$AZYI-!YSJ3AxALSLO-!$A8LSS3dAGI$8QKL!LJ$OFSY=ALSLO-J-K$A-ALxJYtLJ-!L>--AGIY>$QQYx
xLMSYAYJt$J-JFAnJYA-SUYItLJKLAS$AJYOFKYAQGYQYhQJxW$JAIL!x-J-BAJ$dSYOYZ-=ASYAAUYIt-IW$JASYx3$AGY8dY83AKAI$E$S-BAQY>-
LOFS3dACKYSYt-n$QK-dA-ACKYOYZ-n$QKdAGIYhO$tA8$OLRAt-IAhYO$$A-ACUU$KJ-xS3t'''

# Подсчёт частот символов в тексте
freq_dict = calculate_frequency(encrypted_text)

# Сохранение частот в файл
save_frequency_to_json('encrypted_freq.json', freq_dict)

# Печать результата
print("Частотный анализ текста:")
print(freq_dict)
