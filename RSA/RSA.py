import random
import math
def sieve_of_eratosthenes(limit):
    is_prime = [True] * (limit + 1)  # Массив знаков, где True означает, что число потенциально простое
    is_prime[0] = is_prime[1] = False  # 0 и 1 не простые числа

    for num in range(2, int(limit**0.5) + 1):
        if is_prime[num]:  # Если число простое
            for multiple in range(num*num, limit + 1, num):
                is_prime[multiple] = False  # Помечаем все кратные числа как непростые

    primes = [num for num, prime in enumerate(is_prime) if prime]
    return primes
PRIMES = sieve_of_eratosthenes(1000000)

def extended_gcd(a, b):
    """Расширенный алгоритм Евклида"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    """Модулярная инверсия"""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        return None  # Обратного элемента не существует
    else:
        return x % m

def generate_keys(bit_length=None):
    """Генерация ключей RSA"""
    # Выбираем два разных случайных простых числа
    p = random.choice(PRIMES)
    q = random.choice(PRIMES)
    while q == p:
        q = random.choice(PRIMES)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Выбираем e взаимно простое с phi
    e = 65537
    while math.gcd(e, phi) != 1:
        e = random.choice([3, 5, 17, 257, 65537])
    
    d = modinv(e, phi)
    
    public_key = (n, e)
    private_key = (n, d)
    
    return public_key, private_key, p, q

def encrypt(message, public_key):
    """Шифрование сообщения"""
    n, e = public_key
    
    if isinstance(message, str):
        # Преобразуем строку в последовательность чисел
        message_bytes = message.encode('utf-8')
        blocks = []
        for i in range(0, len(message_bytes), 3):  # Блоки по 3 байта
            block = message_bytes[i:i+3]
            m = int.from_bytes(block, 'big')
            blocks.append(m)
    else:
        blocks = [message]
    
    cipher_blocks = []
    for m in blocks:
        if m >= n:
            raise ValueError(f"Сообщение {m} слишком велико для модуля n={n}")
        c = pow(m, e, n)
        cipher_blocks.append(c)
    
    return cipher_blocks

def decrypt(cipher_blocks, private_key):
    """Дешифрование сообщения"""
    n, d = private_key
    message_blocks = []
    
    for c in cipher_blocks:
        m = pow(c, d, n)
        message_blocks.append(m)
    
    # Собираем байты обратно в строку
    message_bytes = bytearray()
    for m in message_blocks:
        # Определяем, сколько байт нужно для представления числа m
        length = (m.bit_length() + 7) // 8
        message_bytes.extend(m.to_bytes(length, 'big'))
    
    # Преобразуем байты обратно в строку
    return message_bytes.decode('utf-8', 'ignore')  # Используем ignore, чтобы игнорировать возможные ошибки декодирования

def main():
    print("RSA с простыми числами до 1,000,000")
    print(f"Всего простых чисел в базе: {len(PRIMES)}")
    
    # Генерация ключей
    public_key, private_key, p, q = generate_keys()
    print(f"\nВыбранные простые числа:\np = {p}\nq = {q}")
    print(f"\nОткрытый ключ (n, e):\nn = {public_key[0]}\ne = {public_key[1]}")
    print(f"\nЗакрытый ключ (n, d):\nn = {private_key[0]}\nd = {private_key[1]}")
    
    # Ввод сообщения
    message = input("\nВведите сообщение для шифрования: ")
    # Шифрование
    cipher_blocks = encrypt(message, public_key)
    print(f"\nЗашифрованное сообщение (числовые блоки): {cipher_blocks}")
        
    # Дешифрование
    decrypted = decrypt(cipher_blocks, private_key)
    print(f"\nРасшифрованное сообщение: {decrypted}")

if __name__ == "__main__":
    main()

 