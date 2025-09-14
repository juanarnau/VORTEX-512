# keygen.py

import os
import secrets
import hashlib
import base64

KEY_SIZE = 64  # 512 bits

def generate_random_key():
    """Genera una clave aleatoria de 512 bits."""
    return secrets.token_bytes(KEY_SIZE)

def generate_key_hex():
    """Clave aleatoria en formato hexadecimal."""
    return generate_random_key().hex()

def generate_key_base64():
    """Clave aleatoria en formato base64."""
    return base64.b64encode(generate_random_key()).decode()

def derive_key_from_password(password: str, salt: bytes = None, iterations: int = 100_000):
    """Deriva una clave de 512 bits desde una contraseña usando PBKDF2."""
    if salt is None:
        salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha512', password.encode(), salt, iterations, dklen=KEY_SIZE)
    return key, salt