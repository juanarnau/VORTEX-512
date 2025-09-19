# vortex_storage/file_handler.py

import os

def validate_input_file(path: str) -> bool:
    """Verifica que el archivo de entrada exista y sea legible."""
    return os.path.isfile(path)

def suggest_decrypted_name(path: str) -> str:
    """Sugiere un nombre para el archivo descifrado."""
    if path.endswith(".jvtex"):
        return path[:-6] + "_descifrado.txt"
    return path + "_descifrado.txt"

def ensure_directory_exists(path: str):
    """Crea el directorio si no existe."""
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

def prevent_overwrite(path: str) -> str:
    """Evita sobrescribir archivos existentes, añadiendo sufijos si es necesario."""
    base, ext = os.path.splitext(path)
    counter = 1
    new_path = path
    while os.path.exists(new_path):
        new_path = f"{base}_{counter}{ext}"
        counter += 1
    return new_path