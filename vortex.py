# -*- coding: utf-8 -*-
"""
Juan Arnau

"""
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import hashlib, os, zipfile, shutil

# --- VORTEX-512 simplificado ---
def expand_key(master_key, rounds):
    subkeys = []
    for i in range(rounds):
        data = master_key + i.to_bytes(2, 'big')
        subkey = hashlib.sha3_256(data).digest()
        subkeys.append(subkey)
    return subkeys

def substitution(block, subkey):
    return bytes([(b ^ subkey[i % len(subkey)]) for i, b in enumerate(block)])

def permutation(block):
    return block[::-1]

def vortex_encrypt(data, key, block_size=32, rounds=10):
    subkeys = expand_key(key, rounds)
    padding_len = block_size - (len(data) % block_size)
    data += bytes([padding_len]) * padding_len
    blocks = [data[i:i+block_size] for i in range(0, len(data), block_size)]
    encrypted = []
    for block in blocks:
        state = block
        for i in range(rounds):
            state = substitution(state, subkeys[i])
            state = permutation(state)
        encrypted.append(state)
    return b''.join(encrypted)

def vortex_decrypt(data, key, block_size=32, rounds=10):
    subkeys = expand_key(key, rounds)
    blocks = [data[i:i+block_size] for i in range(0, len(data), block_size)]
    decrypted = []
    for block in blocks:
        state = block
        for i in reversed(range(rounds)):
            state = permutation(state)
            state = substitution(state, subkeys[i])
        decrypted.append(state)
    data = b''.join(decrypted)
    padding_len = data[-1]
    return data[:-padding_len]

def derive_key(password, salt, iterations=100_000):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations, dklen=32)

def hash_sha256(data):
    return hashlib.sha256(data).digest()

def comprimir_carpeta(ruta_carpeta, ruta_zip):
    with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for carpeta_raiz, _, archivos in os.walk(ruta_carpeta):
            for archivo in archivos:
                ruta_completa = os.path.join(carpeta_raiz, archivo)
                ruta_relativa = os.path.relpath(ruta_completa, ruta_carpeta)
                zipf.write(ruta_completa, ruta_relativa)

def descomprimir_zip(ruta_zip, destino):
    with zipfile.ZipFile(ruta_zip, 'r') as zipf:
        zipf.extractall(destino)
        
def cifrar_archivo():
    ruta = filedialog.askopenfilename()
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
    messagebox.showinfo("Éxito", f"Archivo cifrado:\n{salida}")

def descifrar_archivo():
    ruta = filedialog.askopenfilename(filetypes=[("Archivos JVSEC", "*.jvsec")])
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
        messagebox.showinfo("Éxito", f"Archivo descifrado:\n{salida}")
    except:
        messagebox.showerror("Error", "Contraseña incorrecta o archivo dañado.")

def cifrar_carpeta():
    carpeta = filedialog.askdirectory()
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
    messagebox.showinfo("Éxito", f"Carpeta cifrada:\n{salida}")

def descifrar_carpeta():
    ruta = filedialog.askopenfilename(filetypes=[("Archivos JVSEC", "*.jvsec")])
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
            raise ValueError("Integridad comprometida.")
        temp_zip = ruta.replace(".jvsec", "_restaurado.zip")
        with open(temp_zip, 'wb') as f:
            f.write(datos)
        destino = ruta.replace(".jvsec", "_carpeta")
        os.makedirs(destino, exist_ok=True)
        descomprimir_zip(temp_zip, destino)
        os.remove(temp_zip)
        messagebox.showinfo("Éxito", f"Carpeta restaurada:\n{destino}")
    except:
        messagebox.showerror("Error", "Contraseña incorrecta o archivo dañado.")

def iniciar_ventana_principal(root):
    root.deiconify()
    root.title("🛡️ VORTEX-512 Total Security")

    tk.Label(root, text="Suite de cifrado de archivos y carpetas", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Button(root, text="📄 Cifrar archivo", command=cifrar_archivo, width=30).pack(pady=5)
    tk.Button(root, text="📁 Cifrar carpeta", command=cifrar_carpeta, width=30).pack(pady=5)
    tk.Button(root, text="🔓 Descifrar archivo", command=descifrar_archivo, width=30).pack(pady=5)
    tk.Button(root, text="🔓 Descifrar carpeta", command=descifrar_carpeta, width=30).pack(pady=5)
    tk.Label(root, text="Extensión personalizada: .jvsec", font=("Arial", 10)).pack(pady=5)
    tk.Label(root, text="Creado por Juan · VORTEX-512", font=("Arial", 10)).pack(pady=10)



def mostrar_splash(root):
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    splash.geometry("400x420+500+200")
    splash.configure(bg="#0a1f3d")

    img = Image.open("vortex_logo.png").resize((200, 200))
    logo = ImageTk.PhotoImage(img)
    splash.logo = logo  # Mantener referencia

    tk.Label(splash, image=logo, bg="#0a1f3d").pack(pady=30)
    tk.Label(splash, text="Bienvenido a VORTEX-512", font=("Arial", 14, "bold"), fg="white", bg="#0a1f3d").pack()
    tk.Label(splash, text="Protegiendo tus datos desde el núcleo", font=("Arial", 10), fg="#80cfff", bg="#0a1f3d").pack(pady=5)

    splash.after(3000, splash.destroy)


# --- Ejecutar splash al iniciar ---
mostrar_splash()

# --- Ejecutar la aplicación ---
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal temporalmente

    # Mostrar pantalla de bienvenida y luego abrir la interfaz principal
    mostrar_splash(root)
    root.after(3100, lambda: iniciar_ventana_principal(root))
    root.mainloop()
