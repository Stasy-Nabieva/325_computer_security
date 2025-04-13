import unittest
from Cesar import encrypt

class TestCaesarCipher(unittest.TestCase):

    def test_encryption(self):
        self.assertEqual(encrypt("Hello, World!", 3), "Khoor, Zruog!")
        self.assertEqual(encrypt("abc", 2), "cde")
        self.assertEqual(encrypt("XYZ", 3), "ABC")

    def test_no_shift(self):
        self.assertEqual(encrypt("Hello, World!", 0), "Hello, World!")
        
    def test_non_alpha(self):
        self.assertEqual(encrypt("1234 @#!", 5), "1234 @#!")
        
    def test_empty_string(self):
        self.assertEqual(encrypt("", 3), "")    

if __name__ == "__main__":
    unittest.main()