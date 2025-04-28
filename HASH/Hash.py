import hashlib

def sha256_hash(input_bytes: bytes) -> bytes:
    # функция принимает массив байт произвольной длины и возвращает хеш SHA-256 (32 байта).
    sha256 = hashlib.sha256()
    sha256.update(input_bytes)
    return sha256.digest()

# ввод данных с клавиатуры
if __name__ == "__main__":
    user_input = input("Введите строку для хеширования: ")
    input_bytes = user_input.encode("utf-8")  # преобразование строки в байты
    
    hashed = sha256_hash(input_bytes)
    
    print("\nРезультат:")
    print(f"Входные данные: {user_input}")
    print(f"Хеш SHA-256 (в байтах, длина {len(hashed)}): {hashed}")
    print(f"Хеш SHA-256 (hex): {hashed.hex()}")
