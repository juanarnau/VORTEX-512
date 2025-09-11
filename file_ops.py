# -*- coding: utf-8 -*-
import os
from tkinter import filedialog, messagebox, simpledialog
from crypto import vortex_encrypt, vortex_decrypt
from utils import derive_key, hash_sha256, comprimir_carpeta, descomprimir_zip

def cifrar_archivo():
    ruta = filedialog.askopenfilename(title="Selecciona archivo para cifrar")
    if not ruta: return
    password = simpledialog.askstring("Contraseña", "Introduce una contraseña:", show='*')
    if not password: return

    with open(ruta, 'rb') as f:
        datos = f.read()

    salt = os.urandom(16)
    clave = derive_key(password, salt)
    cifrado = vortex_encrypt(datos, clave)

    salida = ruta + ".jvsec"
    with open(salida, 'wb') as f:
        f.write(salt + cifrado)

    messagebox.showinfo("Éxito", f"Archivo cifrado guardado como:\n{salida}")

def descifrar_archivo():
    ruta = filedialog.askopenfilename(title="Selecciona archivo .jvsec", filetypes=[("Archivos JVSEC", "*.jvsec")])
    if not ruta: return
    password = simpledialog.askstring("Contraseña", "Introduce la contraseña:", show='*')
    if not password: return

    with open(ruta, 'rb') as f:
        contenido = f.read()

    salt = contenido[:16]
    cifrado = contenido[16:]
    clave = derive_key(password, salt)

    try:
        datos = vortex_decrypt(cifrado, clave)
        salida = ruta.replace(".jvsec", ".descifrado")
        with open(salida, 'wb') as f:
            f.write(datos)
        messagebox.showinfo("Éxito", f"Archivo descifrado guardado como:\n{salida}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo descifrar:\n{e}")

def cifrar_carpeta():
    carpeta = filedialog.askdirectory(title="Selecciona carpeta para cifrar")
    if not carpeta: return
    password = simpledialog.askstring("Contraseña", "Introduce una contraseña:", show='*')
    if not password: return

    temp_zip = carpeta + "_temp.zip"
    comprimir_carpeta(carpeta, temp_zip)

    with open(temp_zip, 'rb') as f:
        datos = f.read()
    os.remove(temp_zip)

    salt = os.urandom(16)
    clave = derive_key(password, salt)
    hash_integridad = hash_sha256(datos)
    cifrado = vortex_encrypt(datos, clave)

    salida = carpeta + ".jvsec"
    with open(salida, 'wb') as f:
        f.write(salt + hash_integridad + cifrado)

    messagebox.showinfo("Éxito", f"Carpeta cifrada guardada como:\n{salida}")

def descifrar_carpeta():
    ruta = filedialog.askopenfilename(title="Selecciona archivo .jvsec", filetypes=[("Archivos JVSEC", "*.jvsec")])
    if not ruta: return
    password = simpledialog.askstring("Contraseña", "Introduce la contraseña:", show='*')
    if not password: return

    with open(ruta, 'rb') as f:
        contenido = f.read()

    salt = contenido[:16]
    hash_original = contenido[16:48]
    cifrado = contenido[48:]
    clave = derive_key(password, salt)

    try:
        datos = vortex_decrypt(cifrado, clave)
        if hash_sha256(datos) != hash_original:
            raise ValueError("La verificación de integridad ha fallado.")

        temp_zip = ruta.replace(".jvsec", "_restaurado.zip")
        with open(temp_zip, 'wb') as f:
            f.write(datos)

        destino = ruta.replace(".jvsec", "_carpeta")
        os.makedirs(destino, exist_ok=True)
        descomprimir_zip(temp_zip, destino)
        os.remove(temp_zip)

        messagebox.showinfo("Éxito", f"Carpeta restaurada en:\n{destino}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo descifrar:\n{e}")
