import unittest
from Vigenere import vigenere_encrypt, vigenere_decrypt

class TestVigenereCipher(unittest.TestCase):
    def test_encrypt_basic(self):
        #Тест базового шифрования
        self.assertEqual(vigenere_encrypt("ATTACKATDAWN", "LEMON"), "LXFOPVEFRNHR")
    
    def test_decrypt_basic(self):
        #Тест базового дешифрования
        self.assertEqual(vigenere_decrypt("LXFOPVEFRNHR", "LEMON"), "ATTACKATDAWN")
    
    def test_encrypt_with_spaces(self):
        #Тест шифрования с пробелами
        self.assertEqual(vigenere_encrypt("HELLO WORLD", "KEY"), "RIJVS GSPVH")
    
    def test_encrypt_with_punctuation(self):
        #Тест шифрования с пунктуацией
        self.assertEqual(vigenere_encrypt("Hello, World!", "KEY"), "RIJVS, AMBPB!")
    def test_decrypt_wuth_puntuation(self):
        #Тест дешифрования с пунктуацией
        self.assertEqual(vigenere_decrypt("RIJVS, AMBPB!", "KEY"), "HELLO, WORLD!")
    
    def test_key_longer_than_text(self):
        #Тест с ключом длиннее текста
        self.assertEqual(vigenere_encrypt("ABC", "LONGKEY"), "LPP")
        self.assertEqual(vigenere_decrypt("LPP", "LONGKEY"), "ABC")
    
    def test_case_insensitivity(self):
        #Тест нечувствительности к регистру
        self.assertEqual(vigenere_encrypt("attackatdawn", "lemon"), "LXFOPVEFRNHR")
        self.assertEqual(vigenere_decrypt("lxfopvefrnhr", "LEMON"), "ATTACKATDAWN")
    
    def test_empty_text(self):
        #Тест с пустым текстом
        self.assertEqual(vigenere_encrypt("", "KEY"), "")
        self.assertEqual(vigenere_decrypt("", "KEY"), "")
    
    def test_same_text_key(self):
        #Тест когда текст и ключ одинаковые
        self.assertEqual(vigenere_encrypt("TEST", "TEST"), "MIKM")
        self.assertEqual(vigenere_decrypt("MIKM", "TEST"), "TEST")

if __name__ == "__main__":
    unittest.main()