import unittest
from RSA import encrypt, decrypt, generate_keys, modinv, extended_gcd

class TestRSACryptography(unittest.TestCase):

    def setUp(self):
        # Генерируем ключи перед каждым тестом
        self.public_key, self.private_key, self.p, self.q = generate_keys()

    def test_generate_keys(self):
        self.assertIsInstance(self.public_key, tuple)
        self.assertIsInstance(self.private_key, tuple)
        self.assertIsInstance(self.p, int)
        self.assertIsInstance(self.q, int)
        self.assertNotEqual(self.p, self.q)

    def test_encrypt_decrypt(self):
        message = "Hello, RSA!"
        cipher_blocks = encrypt(message, self.public_key)
        decrypted_message = decrypt(cipher_blocks, self.private_key)

        self.assertEqual(message, decrypted_message)

    def test_encrypt_large_message(self):
        message = "A" * 1000  # Долгое сообщение для шифрования
        cipher_blocks = encrypt(message, self.public_key)
        decrypted_message = decrypt(cipher_blocks, self.private_key)

        self.assertEqual(message, decrypted_message)

    def test_modinv(self):
        a = 3
        m = 11
        self.assertIsNotNone(modinv(a, m))  # Должен вернуть обратный элемент
        self.assertEqual(modinv(a, m) * a % m, 1)

    def test_modinv_non_coprime(self):
        a = 4
        m = 8
        self.assertIsNone(modinv(a, m))  # Должен вернуть None, не существует обратного элемента

    def test_extended_gcd(self):
        a, b = 30, 12
        g, x, y = extended_gcd(a, b)
        self.assertEqual(g, 6)  # gcd(30, 12) = 6
        self.assertEqual(30 * x + 12 * y, g)  # Проверка на корректность

if __name__ == "__main__":
    unittest.main()