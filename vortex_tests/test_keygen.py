# vortex_tests/test_keygen.py

import sys
import os

# Añade la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vortex_core import keygen


def test_random_key():
    key = keygen.generate_random_key()
    print(f"🔑 Clave aleatoria (binaria): {key}")
    assert len(key) == keygen.KEY_SIZE

def test_key_hex():
    key_hex = keygen.generate_key_hex()
    print(f"🔑 Clave en hexadecimal: {key_hex}")
    assert len(key_hex) == keygen.KEY_SIZE * 2  # Cada byte = 2 caracteres hex

def test_key_base64():
    key_b64 = keygen.generate_key_base64()
    print(f"🔑 Clave en base64: {key_b64}")
    assert isinstance(key_b64, str)

def test_derived_key():
    password = "MiContraseñaSegura123!"
    key, salt = keygen.derive_key_from_password(password)
    print(f"🔐 Clave derivada: {key.hex()}")
    print(f"🧂 Salt usado: {salt.hex()}")
    assert len(key) == keygen.KEY_SIZE
    assert len(salt) == 16

if __name__ == "__main__":
    test_random_key()
    test_key_hex()
    test_key_base64()
    test_derived_key()