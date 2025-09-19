import unittest
import os
from vortex_core import vortex_cipher
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vortex_core import vortex_cipher

class TestVortexCipher(unittest.TestCase):

    def setUp(self):
        self.key = os.urandom(64)  # 512 bits
        self.data = b"Este es un mensaje secreto que debe cifrarse correctamente."
        self.iv = os.urandom(64)

    def test_encrypt_decrypt(self):
        encrypted = vortex_cipher.vortex_encrypt(self.data, self.key, self.iv)
        decrypted = vortex_cipher.vortex_decrypt(encrypted, self.key)
        self.assertEqual(decrypted, self.data)

    def test_authentication_failure(self):
        encrypted = vortex_cipher.vortex_encrypt(self.data, self.key, self.iv)
        # Manipular el mensaje cifrado
        tampered = encrypted[:-33] + bytes([encrypted[-33] ^ 0xFF]) + encrypted[-32:]
        with self.assertRaises(ValueError) as context:
            vortex_cipher.vortex_decrypt(tampered, self.key)
        self.assertIn("Autenticación fallida", str(context.exception))

    def test_padding_unpadding(self):
        padded = vortex_cipher.pad_data(self.data)
        unpadded = vortex_cipher.unpad_data(padded)
        self.assertEqual(unpadded, self.data)

    def test_sbox_reversibility(self):
        block = os.urandom(64)
        substituted = vortex_cipher.sbox_substitution(block)
        reversed_block = vortex_cipher.inverse_sbox_substitution(substituted)
        self.assertEqual(reversed_block, block)

if __name__ == '__main__':
    unittest.main()