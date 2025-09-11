# -*- coding: utf-8 -*-
import hashlib
import os
import zipfile

def derive_key(password, salt, iterations=100_000):
    """Genera una clave segura a partir de una contraseña y una sal."""
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations, dklen=32)

def hash_sha256(data):
    """Devuelve el hash SHA-256 de los datos."""
    return hashlib.sha256(data).digest()

def comprimir_carpeta(ruta_carpeta, ruta_zip):
    """Comprime una carpeta en un archivo ZIP."""
    with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for carpeta_raiz, _, archivos in os.walk(ruta_carpeta):
            for archivo in archivos:
                ruta_completa = os.path.join(carpeta_raiz, archivo)
                ruta_relativa = os.path.relpath(ruta_completa, ruta_carpeta)
                zipf.write(ruta_completa, ruta_relativa)

def descomprimir_zip(ruta_zip, destino):
    """Extrae el contenido de un archivo ZIP en la carpeta destino."""
    with zipfile.ZipFile(ruta_zip, 'r') as zipf:
        zipf.extractall(destino)
