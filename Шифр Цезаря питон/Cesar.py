def encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            encrypted_text += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            encrypted_text += char
    return encrypted_text

if __name__ == "__main__":
    user_input = input("Введите текст для шифрования: ")
    shift_value = int(input("Введите значение сдвига: "))
    print("Зашифрованный текст:", encrypt(user_input, shift_value))
