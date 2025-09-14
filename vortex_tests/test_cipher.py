# vortex_tests/test_cipher.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vortex_core import keygen, vortex_cipher

def test_encrypt_decrypt_cbc():
    original_text = "Este es un mensaje secreto que debe cifrarse correctamente. VORTEX-512 en acción.".encode("utf-8")
    key = keygen.generate_random_key()

    print(f"🔐 Clave generada (hex): {key.hex()}")
    print(f"📨 Texto original: {original_text}")

    # Cifrado con IV aleatorio
    encrypted = vortex_cipher.vortex_encrypt(original_text, key)
    print(f"🧊 Texto cifrado (hex): {encrypted.hex()}")

    # Descifrado
    decrypted = vortex_cipher.vortex_decrypt(encrypted, key)
    print(f"📬 Texto descifrado: {decrypted}")

    assert decrypted == original_text
    print("✅ Prueba exitosa: El texto original fue recuperado correctamente.")

if __name__ == "__main__":
    test_encrypt_decrypt_cbc()