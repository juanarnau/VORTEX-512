import os
from cryptography.fernet import Fernet
from vortex.file_crypto import encrypt_file, decrypt_file
from cryptography.fernet import InvalidToken

def encrypt_folder(folder_path: str, key: bytes):
    fernet = Fernet(key)
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                encrypt_file(file_path, fernet)
            except Exception as e:
                print(f"[ERROR] No se pudo cifrar {file_path}: {e}")

def decrypt_folder(folder_path, fernet):
       archivos_descifrados = 0
       for root, _, files in os.walk(folder_path):
           for file in files:
               file_path = os.path.join(root, file)
               # Solo procesar archivos cifrados
               if not file_path.endswith(".encrypted"):
                   continue
               try:
                with open(file_path, "rb") as f:
                    encrypted_data = f.read()
                decrypted_data = fernet.decrypt(encrypted_data)
                output_path = file_path.replace(".encrypted", "")
                with open(output_path, "wb") as f:
                    f.write(decrypted_data)
                archivos_descifrados += 1
               except InvalidToken:
                    raise ValueError("Contraseña incorrecta para descifrar los archivos.")
               except Exception as e:
                    print(f"Error al descifrar {file_path}: {e}")
       return archivos_descifrados