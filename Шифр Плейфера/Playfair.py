import re

class PlayfairCipher:
    def __init__(self, key):
        self.key = key.upper().replace("J", "I")
        self.table = self._create_table()
    
    def _create_table(self):
        # Удаляем повторяющиеся буквы и добавляем остальные алфавитные (I=J)
        key_letters = []
        for char in self.key:
            if char not in key_letters and char.isalpha():
                key_letters.append(char)
        
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        for char in alphabet:
            if char not in key_letters:
                key_letters.append(char)
        
        table = []
        for i in range(5):
            row = key_letters[i*5 : (i+1)*5]
            table.append(row)
        
        return table
    
    def _preprocess_text(self, text):
        # Удаляем все не-алфавитные символы и приводим к верхнему регистру
        text = re.sub(r'[^A-Za-z]', '', text).upper()
        text = text.replace("J", "I")
        
        # Разбиваем на биграммы и добавляем X между повторяющимися буквами
        processed = []
        i = 0
        while i < len(text):
            if i == len(text) - 1:
                # Если нечетное количество символов, добавляем X
                processed.append(text[i] + 'X')
                i += 1
            elif text[i] == text[i+1]:
                # Повторяющиеся буквы - добавляем X между ними
                processed.append(text[i] + 'X')
                i += 1
            else:
                processed.append(text[i] + text[i+1])
                i += 2
        return processed
    
    def _find_position(self, char):
        for row in range(5):
            for col in range(5):
                if self.table[row][col] == char:
                    return (row, col)
        raise ValueError(f"Символ {char} не найден в таблице")
    
    def encrypt(self, plaintext):
        bigrams = self._preprocess_text(plaintext)
        ciphertext = []
        
        for a, b in bigrams:
            row1, col1 = self._find_position(a)
            row2, col2 = self._find_position(b)
            
            if row1 == row2:
                # Одна строка - сдвигаем вправо
                ciphertext.append(self.table[row1][(col1 + 1) % 5] + self.table[row2][(col2 + 1) % 5])
            elif col1 == col2:
                # Один столбец - сдвигаем вниз
                ciphertext.append(self.table[(row1 + 1) % 5][col1] + self.table[(row2 + 1) % 5][col2])
            else:
                # Прямоугольник - берем противоположные углы
                ciphertext.append(self.table[row1][col2] + self.table[row2][col1])
        
        return ''.join(ciphertext)
    
    def decrypt(self, ciphertext):
        # Проверяем, что ciphertext имеет четную длину и состоит только из букв
        ciphertext = re.sub(r'[^A-Z]', '', ciphertext.upper())
        if len(ciphertext) % 2 != 0:
            raise ValueError("Длина зашифрованного текста должна быть четной")
        
        bigrams = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
        plaintext = []
        
        for a, b in bigrams:
            row1, col1 = self._find_position(a)
            row2, col2 = self._find_position(b)
            
            if row1 == row2:
                # Одна строка - сдвигаем влево
                plaintext.append(self.table[row1][(col1 - 1) % 5] + self.table[row2][(col2 - 1) % 5])
            elif col1 == col2:
                # Один столбец - сдвигаем вверх
                plaintext.append(self.table[(row1 - 1) % 5][col1] + self.table[(row2 - 1) % 5][col2])
            else:
                # Прямоугольник - берем противоположные углы
                plaintext.append(self.table[row1][col2] + self.table[row2][col1])
        
        # Удаляем добавленные X при шифровании (если они есть)
        decrypted = ''.join(plaintext)
        if decrypted.endswith('X'):
            decrypted = decrypted[:-1]
        
        # Удаляем X между повторяющимися буквами
        i = 1
        while i < len(decrypted) - 1:
            if decrypted[i] == 'X' and decrypted[i-1] == decrypted[i+1]:
                decrypted = decrypted[:i] + decrypted[i+1:]
            else:
                i += 1
        
        return decrypted
    
    def get_table(self):
        return self.table

if __name__ == "__main__":
    key = "PLAYFAIR EXAMPLE"
    cipher = PlayfairCipher(key)
    
    print("Таблица Плейфера:")
    for row in cipher.get_table():
        print(' '.join(row))
    
    plaintext = input("\nИсходный текст:", )
    encrypted = cipher.encrypt(plaintext)
    print("Зашифрованный текст:", encrypted)
    decrypted = cipher.decrypt(encrypted)
    print("Расшифрованный текст:", decrypted)
    
