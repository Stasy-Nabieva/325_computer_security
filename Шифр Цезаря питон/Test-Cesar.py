import unittest
from Cesar import encrypt
from Cesar import decrypt

class TestEncryptionDecryption(unittest.TestCase):

    def test_encryption(self):
        self.assertEqual(encrypt("Hello, World!", 3), "Khoor, Zruog!")
        self.assertEqual(encrypt("abc", 1), "bcd")
        self.assertEqual(encrypt("xyz", 3), "abc")
      
    
    def test_decryption(self):
        self.assertEqual(decrypt("Khoor, Zruog!", 3), "Hello, World!")
        self.assertEqual(decrypt("bcd", 1), "abc")
        self.assertEqual(decrypt("abc", 3), "xyz")

    def test_no_shift(self):
        self.assertEqual(encrypt("No Shift", 0), "No Shift")
        self.assertEqual(decrypt("No Shift", 0), "No Shift")

    def test_non_alpha_characters(self):
        self.assertEqual(encrypt("Hello, World 123!", 5), "Mjqqt, Btwqi 123!")
        self.assertEqual(decrypt("Mjqqt, Btwqi 123!", 5), "Hello, World 123!")

if __name__ == "__main__":
    unittest.main() 
