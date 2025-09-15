import os
from cryptography.fernet import Fernet
from vortex.file_crypto import encrypt_file, decrypt_file

def encrypt_folder(folder_path: str, key: bytes):
    fernet = Fernet(key)
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                encrypt_file(file_path, fernet)
            except Exception as e:
                print(f"[ERROR] No se pudo cifrar {file_path}: {e}")

def decrypt_folder(folder_path: str, key: bytes):
    fernet = Fernet(key)
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                decrypt_file(file_path, fernet)
            except Exception as e:
                print(f"[ERROR] No se pudo descifrar {file_path}: {e}")