def permutation_cipher(text, key, fill_char='*'):
    """
    Шифрует текст методом перестановки с использованием таблицы.
    
    :param text: Исходный текст (без пробелов)
    :param key: Порядок столбцов (например, [2, 1, 3])
    :param fill_char: Символ для заполнения пустых ячеек
    :return: Зашифрованная строка
    """
    key = [k - 1 for k in key]  # Переводим ключ в индексы (с 0)
    cols = len(key)
    
    # Дополняем текст, чтобы делился на число столбцов
    remainder = len(text) % cols
    if remainder != 0:
        text += fill_char * (cols - remainder)
    
    # Разбиваем текст на строки таблицы
    rows = [text[i * cols : (i + 1) * cols] for i in range(len(text) // cols)]
    
    # Шифруем: считываем столбцы в порядке ключа
    cipher_text = []
    for row in rows:
        for col_index in key:
            if col_index < len(row):
                cipher_text.append(row[col_index])
    
    return ''.join(cipher_text)


def decrypt_permutation(cipher_text, key, fill_char='*'):
    """
    Расшифровывает текст, зашифрованный перестановкой.
    
    :param cipher_text: Зашифрованный текст
    :param key: Порядок столбцов при шифровании
    :param fill_char: Символ, который использовался для заполнения
    :return: Исходный текст (без fill_char в конце)
    """
    key = [k - 1 for k in key]
    cols = len(key)
    rows = len(cipher_text) // cols
    
    # Восстанавливаем исходный порядок столбцов
    inverse_key = [0] * cols
    for i, k in enumerate(key):
        inverse_key[k] = i
    
    # Разбиваем зашифрованный текст на строки
    cipher_rows = [cipher_text[i * cols : (i + 1) * cols] for i in range(rows)]
    
    # Восстанавливаем исходные строки
    plain_text = []
    for row in cipher_rows:
        # Сортируем символы строки в исходном порядке
        sorted_row = [''] * cols
        for i, pos in enumerate(inverse_key):
            if i < len(row):
                sorted_row[pos] = row[i]
        plain_text.append(''.join(sorted_row))
    
    decrypted = ''.join(plain_text)
    # Удаляем символы заполнения (если они были)
    if fill_char in decrypted:
        decrypted = decrypted.rstrip(fill_char)
    
    return decrypted


def get_key_from_input():
    """
    Запрашивает ключ у пользователя с клавиатуры.
    Пример ввода: "2 1 3" → [2, 1, 3]
    """
    while True:
        try:
            key_input = input("Введите ключ (через пробел, например, '2 1 3'): ").strip()
            key = list(map(int, key_input.split()))
            if len(key) == 0:
                raise ValueError("Ключ не может быть пустым")
            return key
        except ValueError as e:
            print(f"Ошибка: {e}. Попробуйте снова.")


def main():
    """Интерактивный режим для шифрования/расшифровки."""
    mode = input("Выберите режим (1 - шифрование, 2 - расшифровка): ").strip()
    
    if mode == "1":
        text = input("Введите текст для шифрования: ").replace(" ", "")
        key = get_key_from_input()
        encrypted = permutation_cipher(text, key)
        print(f"Зашифрованный текст: {encrypted}")
    elif mode == "2":
        cipher_text = input("Введите текст для расшифровки: ").replace(" ", "")
        key = get_key_from_input()
        decrypted = decrypt_permutation(cipher_text, key)
        print(f"Расшифрованный текст: {decrypted}")
    else:
        print("Неверный режим. Завершение программы.")


if __name__ == "__main__":
    main()