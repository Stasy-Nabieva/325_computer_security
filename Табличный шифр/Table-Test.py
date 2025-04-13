import unittest
from unittest.mock import patch
from Table import permutation_cipher,decrypt_permutation, get_key_from_input
    
class TestPermutationCipher(unittest.TestCase):

    def test_encryption(self):
        self.assertEqual(permutation_cipher("HELLO", [2, 1]), "EHLL*O")
        self.assertEqual(permutation_cipher("WORLD", [1, 3, 2]), "WROL*D")
        
    def test_decryption(self):
        self.assertEqual(decrypt_permutation("EHLL*O", [2, 1]), "HELLO")
        self.assertEqual(decrypt_permutation("WROL*D", [1, 3, 2]), "WORLD")

   
    @patch('builtins.input', side_effect=["2 1 3"])
    def test_get_key_from_input(self, mock_input):
        self.assertEqual(get_key_from_input(), [2, 1, 3])
        
    @patch('builtins.input', side_effect=["wrong input", "2 1"])
    def test_get_key_from_input_with_invalid_input(self, mock_input):
        self.assertEqual(get_key_from_input(), [2, 1])

if __name__ == "__main__":
    unittest.main()
