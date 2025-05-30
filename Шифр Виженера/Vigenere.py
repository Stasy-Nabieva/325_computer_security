def vigenere_encrypt(plaintext, key):
    encrypted_text = []
    key_length = len(key)
    key = key.upper()
    plaintext = plaintext.upper()
    
    for i, char in enumerate(plaintext):
        if char.isalpha():
            shift = ord(key[i % key_length]) - ord('A')
            encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            encrypted_text.append(encrypted_char)
        else:
            encrypted_text.append(char)
    
    return ''.join(encrypted_text)

def vigenere_decrypt(ciphertext, key):

    decrypted_text = []
    key_length = len(key)
    key = key.upper()
    ciphertext = ciphertext.upper()
    
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            shift = ord(key[i % key_length]) - ord('A')
            decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(char)
    
    return ''.join(decrypted_text)

if __name__ == "__main__":
    message = input("Введите сообщение для шифрования (английские буквы): ")
    key = input("Введите ключ (английские буквы): ")
    
    # Проверка на пустой ввод
    if not message or not key:
        print("Ошибка: сообщение и ключ не могут быть пустыми!")
        exit()
    
    if not key.isalpha():
        print("Ошибка: ключ должен содержать только буквы английского алфавита!")
        exit()
    
    print(f"\nИсходное сообщение: {message}")
    print(f"Ключ: {key}")
    
    encrypted = vigenere_encrypt(message, key)
    print(f"Зашифрованное сообщение: {encrypted}")

    decrypted = vigenere_decrypt(encrypted, key)
    print(f"Расшифрованное сообщение: {decrypted}")