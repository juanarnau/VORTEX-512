import unittest
import os
import shutil
from vortex.folder_crypto import encrypt_folder, decrypt_folder
from vortex_core import vortex_cipher

class TestFolderCrypto(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_data"
        self.key = os.urandom(64)  # 512 bits

        os.makedirs(self.test_dir, exist_ok=True)
        # Crear archivos de prueba
        for i in range(3):
            with open(os.path.join(self.test_dir, f"archivo{i}.txt"), "wb") as f:
                f.write(f"Contenido secreto {i}".encode())

    def tearDown(self):
        # Eliminar archivos y carpetas generadas
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_encrypt_decrypt_folder(self):
        # Cifrar
        cifrados = encrypt_folder(self.test_dir, self.key)
        self.assertEqual(cifrados, 3)

        # Verificar que los archivos .vortex existen
        vortex_files = [f for f in os.listdir(self.test_dir) if f.endswith(".vortex")]
        self.assertEqual(len(vortex_files, ), 3)

        # Descifrar
        descifrados = decrypt_folder(self.test_dir, self.key)
        self.assertEqual(descifrados, 3)

        # Verificar contenido original
        for i in range(3):
            with open(os.path.join(self.test_dir, f"archivo{i}.txt"), "rb") as f:
                contenido = f.read().decode()
                self.assertEqual(contenido, f"Contenido secreto {i}")

    def test_authentication_failure(self):
        encrypt_folder(self.test_dir, self.key)
        # Corromper un archivo cifrado
        vortex_path = os.path.join(self.test_dir, "archivo0.txt.vortex")
        with open(vortex_path, "rb") as f:
            data = bytearray(f.read())
        data[-10] ^= 0xFF  # Modificar un byte
        with open(vortex_path, "wb") as f:
            f.write(data)

        # Descifrar debería fallar
        with self.assertRaises(ValueError):
            decrypt_folder(self.test_dir, self.key)

if __name__ == "__main__":
    unittest.main()