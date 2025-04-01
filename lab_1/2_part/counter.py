from collections import Counter

# Зашифрованный текст
encrypted_text = """Y8S-tA-!AYQSYxS3dAGYSRJ-=A-SUYItLJ-K-ARxOR$JQRALOZYIJtAJYA$QJFAGYQO$8YxLJ$OFSYQJFA8$=QJx-=A8ORAI$E$SRA!L8LnCUU$KJ-xS3$ALOZYI-Jt3AGYtYZLBJAYGJ-t-!-
IYxLJFAILhYJWAGIYZILttA-AQQJ$tAnJYAYQYh$SSYALKJWLOFSYAxACGYdWAhYOFEdA8LSS3d
GIYZILtt-IYxLS-
$AxAQxYBAYn$I$8FAGY!xYOR$JAQY!8LxLJFAGI-OYM$S-RAAQ-QJ$t3AKYJYI3$ALxJYtLJ-!-IWBJAIWJ-SS3$A!L8Ln-AYh$QG$nxLRAW8YhQJxYA-AQKYIYQJFAx3GYOS$S-RAYG$IL>-=
QAIL!x-J-$tAJ$dSYOYZ-=AJLK-dAKLKA-QKWQQJx$SS3=ASJ$OO$KJA-AtLE-SSY$AYhWn$S-$A-SUYItLJ-KLAQJLSYxJQRA$9$AhYO$$AxLMSY=
CJ-ASLGILxO$S-RAYJKI3xLBJASYx3$AZYI-!YSJ3AxALSLO-
!$A8LSS3dAGI$8QKL!LJ$OFSY=ALSLO-J-K$A-ALxJYtLJ-!L>--"""


# Функция для подсчета частоты символов
def calculate_frequency(text):
    # Подсчитываем количество каждого символа
    counter = Counter(text)

    # Общая длина текста
    total_chars = len(text)

    # Считаем частоту каждого символа
    freq = {char: count / total_chars for char, count in counter.items()}

    return freq


# Получаем частоты символов
encrypted_freq = calculate_frequency(encrypted_text)

# Выводим частоты символов
for char, freq in encrypted_freq.items():
    print(f"'{char}': {freq:.6f}")
