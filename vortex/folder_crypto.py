import os
from vortex_core import vortex_cipher

def encrypt_folder(folder_path: str, key: bytes) -> int:
    """
    Cifra todos los archivos dentro de una carpeta usando vortex_cipher con autenticación.
    Devuelve el número de archivos cifrados.
    """
    archivos_cifrados = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            # Evitar cifrar archivos ya cifrados
            if file_path.endswith(".vortex"):
                continue

            try:
                with open(file_path, "rb") as f:
                    data = f.read()
                encrypted_data = vortex_cipher.vortex_encrypt(data, key)
                encrypted_path = file_path + ".vortex"
                with open(encrypted_path, "wb") as f:
                    f.write(encrypted_data)
                archivos_cifrados += 1
            except Exception as e:
                print(f"❌ Error al cifrar {file_path}: {e}")
    return archivos_cifrados
import os
from vortex_core import vortex_cipher

def decrypt_folder(folder_path: str, key: bytes) -> int:
    """
    Descifra todos los archivos .vortex dentro de una carpeta usando vortex_cipher con verificación HMAC.
    Devuelve el número de archivos descifrados.
    """
    archivos_descifrados = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            if not file_path.endswith(".vortex"):
                continue

            try:
                with open(file_path, "rb") as f:
                    encrypted_data = f.read()
                decrypted_data = vortex_cipher.vortex_decrypt(encrypted_data, key)
                output_path = file_path.replace(".vortex", "")
                with open(output_path, "wb") as f:
                    f.write(decrypted_data)
                archivos_descifrados += 1
            except ValueError as e:
                print(f"❌ Error al descifrar {file_path}: {e}")
                raise
            except Exception as e:
                print(f"❌ Error inesperado en {file_path}: {e}")


    return archivos_descifrados