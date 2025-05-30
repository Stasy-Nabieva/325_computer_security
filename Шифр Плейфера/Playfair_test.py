import unittest
from Playfair import PlayfairCipher

class TestPlayfairCipher(unittest.TestCase):
    def setUp(self):
        # Общий ключ для нескольких тестов
        self.key = "PLAYFAIR EXAMPLE"
        self.cipher = PlayfairCipher(self.key)
    
    def test_table_creation(self):
        """Проверка правильности создания таблицы"""
        expected_table = [
            ['P', 'L', 'A', 'Y', 'F'],
            ['I', 'R', 'E', 'X', 'M'],
            ['B', 'C', 'D', 'G', 'H'],
            ['K', 'N', 'O', 'Q', 'S'],
            ['T', 'U', 'V', 'W', 'Z']
        ]
        self.assertEqual(self.cipher.get_table(), expected_table)
        
        # Проверка обработки буквы J
        cipher_j = PlayfairCipher("JACK")
        self.assertNotIn('J', [char for row in cipher_j.get_table() for char in row])
    
    def test_preprocess_text(self):
        """Проверка предварительной обработки текста"""
        # Проверка удаления не-алфавитных символов
        self.assertEqual(self.cipher._preprocess_text("Hello, World!"), ['HE', 'LX', 'LO', 'WO', 'RL', 'DX'])
        
        # Проверка замены J на I
        self.assertEqual(self.cipher._preprocess_text("Jazz"), ['IA', 'ZX', 'ZX'])
        
        # Проверка добавления X между повторяющимися буквами
        self.assertEqual(self.cipher._preprocess_text("Letter"), ['LE', 'TX', 'TE', 'RX'])
        
        # Проверка добавления X для нечетной длины
        self.assertEqual(self.cipher._preprocess_text("Odd"), ['OD', 'DX'])
    
    def test_encrypt_decrypt(self):
        """Проверка шифрования и дешифрования"""
        test_cases = [
            ("Hide the gold in the tree stump", "BMODZBXDNABEKUDMUIXMMOUVIF"),
            ("ATTACK AT DAWN", "PVVPBNPVOEUQ"),
            ("HELLO", "DMYRAN"),
            ("PYTHON", "LFZBQO"),
            ("UNITTEST", "LUBPVIKZ")
        ]
        
        for plaintext, expected_cipher in test_cases:
            encrypted = self.cipher.encrypt(plaintext)
            self.assertEqual(encrypted, expected_cipher)
            
            decrypted = self.cipher.decrypt(encrypted)
            # Удаляем X которые могли быть добавлены при шифровании для сравнения
            cleaned_plaintext = plaintext.upper().replace("J", "I")
            cleaned_plaintext = ''.join(filter(str.isalpha, cleaned_plaintext))
            cleaned_decrypted = decrypted.replace("X", "")
            self.assertEqual(cleaned_decrypted, cleaned_plaintext)
    
    def test_special_cases(self):
        """Проверка специальных случаев"""
        # Пустой текст
        self.assertEqual(self.cipher.encrypt(""), "")
        self.assertEqual(self.cipher.decrypt(""), "")
        
        # Текст с только одной буквой
        self.assertEqual(self.cipher.encrypt("A"), "YE")
        self.assertEqual(self.cipher.decrypt("YE"), "A")
        
        # Текст с несколькими J
        self.assertEqual(self.cipher.encrypt("JJJ"), "RMRMRM")
        self.assertEqual(self.cipher.decrypt("RMRMRM"), "III")
    
    def test_find_position(self):
        """Проверка поиска позиции символа в таблице"""
        self.assertEqual(self.cipher._find_position('P'), (0, 0))
        self.assertEqual(self.cipher._find_position('Z'), (4, 4))
        self.assertEqual(self.cipher._find_position('I'), (1, 0))  # J должен быть заменен на I
        
        # Проверка на несуществующий символ
        with self.assertRaises(ValueError):
            self.cipher._find_position('1')
    
    def test_decrypt_with_invalid_input(self):
        """Проверка обработки неверного ввода при дешифровании"""
        # Нечетная длина зашифрованного текста
        with self.assertRaises(ValueError):
            self.cipher.decrypt("ABC")
        
        # Не-алфавитные символы
        self.assertEqual(self.cipher.decrypt("BM,OD ZBXD!"), "HIDETHEG")

if __name__ == '__main__':
    unittest.main()