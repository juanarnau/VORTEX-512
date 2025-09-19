from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def save_key(key: bytes, path: str = "clave.key"):
    with open(path, "wb") as f:
        f.write(key)

def encrypt_file(file_path: str, fernet: Fernet):
    with open(file_path, "rb") as f:
        data = f.read()
    encrypted = fernet.encrypt(data)
    with open(file_path, "wb") as f:
        f.write(encrypted)

def decrypt_file(file_path: str, fernet: Fernet):
    with open(file_path, "rb") as f:
        data = f.read()
    decrypted = fernet.decrypt(data)
    with open(file_path, "wb") as f:
        f.write(decrypted)