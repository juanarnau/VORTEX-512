import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_FILES # type: ignore
from tkinter import filedialog, messagebox
from vortex_core import keygen
from vortex_storage import encryptor
import hashlib, os
import os
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VortexApp:
    def __init__(self, root):
        self.root = root
        self.root.drop_target_register(DND_FILES)  # ✅ Ahora sí está dentro de un método
        self.root.dnd_bind('<<Drop>>', self.handle_drop)
        self.build_interface()


    def __init__(self, root):
        self.root = root
        self.root.title("VORTEX-512 Encryption Suite")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        try:
            self.root.iconbitmap("docs/assets/logo.ico")
        except:
            pass

        self.file_path = ctk.StringVar()
        self.key = None
        self.modo_cifrado = ctk.StringVar(value="clave")

        self.build_interface()

    def build_interface(self):
        ctk.CTkLabel(self.root, text="Archivo a procesar:", font=("Segoe UI", 14), text_color="#E0E0E0").pack(pady=10)

        self.entry = ctk.CTkEntry(self.root, textvariable=self.file_path, width=400)
        self.entry.pack(pady=5)

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self.handle_drop)

        ctk.CTkButton(self.root, text="📂 Seleccionar archivo", command=self.select_file).pack(pady=5)

        ctk.CTkLabel(self.root, text="Modo de cifrado:", font=("Segoe UI", 12)).pack(pady=5)
        ctk.CTkOptionMenu(self.root, variable=self.modo_cifrado, values=["clave", "contraseña"]).pack()

        ctk.CTkButton(self.root, text="🔐 Cifrar archivo", command=self.encrypt_file).pack(pady=10)
        ctk.CTkButton(self.root, text="🔓 Descifrar archivo", command=self.decrypt_file).pack(pady=5)

        key_frame = ctk.CTkFrame(self.root)
        key_frame.pack(pady=10)

        ctk.CTkButton(key_frame, text="💾 Guardar clave", command=self.save_key).grid(row=0, column=0, padx=5)
        ctk.CTkButton(key_frame, text="📁 Cargar clave", command=self.load_key).grid(row=0, column=1, padx=5)

        self.progress = ctk.CTkProgressBar(self.root, width=500)
        self.progress.set(0)
        self.progress.pack(pady=15)

        ctk.CTkButton(self.root, text="❌ Salir", command=self.root.quit).pack(pady=5)

    def handle_drop(self, event):
        dropped_path = event.data.strip().replace("{", "").replace("}", "")
        self.file_path.set(dropped_path)

    def select_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.file_path.set(path)

    def solicitar_contraseña_con_salida(self):
        clave_resultado = []
        salt_resultado = []
        contraseña_resultado = []

        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Introduce la contraseña")
        ventana.geometry("300x200")
        ventana.grab_set()

        ctk.CTkLabel(ventana, text="Contraseña:").pack(pady=5)
        entry1 = ctk.CTkEntry(ventana, show="*")
        entry1.pack()

        ctk.CTkLabel(ventana, text="Repetir contraseña:").pack(pady=5)
        entry2 = ctk.CTkEntry(ventana, show="*")
        entry2.pack()

        def confirmar():
            if entry1.get() != entry2.get():
                messagebox.showerror("Error", "Las contraseñas no coinciden.")
            elif len(entry1.get()) < 6:
                messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres.")
            else:
                contraseña_resultado.append(entry1.get())
                salt = os.urandom(16)
                clave = self.derivar_clave_desde_contraseña(entry1.get(), salt)
                clave_resultado.append(clave)
                salt_resultado.append(salt)
                ventana.destroy()

        ctk.CTkButton(ventana, text="Confirmar", command=confirmar).pack(pady=10)
        ventana.wait_window()

        if clave_resultado and salt_resultado and contraseña_resultado:
            return contraseña_resultado[0], salt_resultado[0]
        return None, None
    def pedir_contraseña(self):
        resultado = []

        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Introduce la contraseña")
        ventana.geometry("300x150")
        ventana.grab_set()

        ctk.CTkLabel(ventana, text="Contraseña:").pack(pady=5)
        entry = ctk.CTkEntry(ventana, show="*")
        entry.pack()

        def confirmar():
            if len(entry.get()) < 6:
                messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres.")
            else:
                resultado.append(entry.get())
                ventana.destroy()

        ctk.CTkButton(ventana, text="Confirmar", command=confirmar).pack(pady=10)
        ventana.wait_window()

        return resultado[0] if resultado else None

    def derivar_clave_desde_contraseña(self, contraseña, salt):
        return hashlib.pbkdf2_hmac("sha512", contraseña.encode(), salt, 100000, dklen=64)

    def save_key(self):
        if not self.key:
            messagebox.showerror("Error", "No hay clave generada.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".key", filetypes=[("Archivo de clave", "*.key")])
        if path:
            with open(path, "wb") as f:
                f.write(self.key)
            messagebox.showinfo("Clave guardada", f"Clave guardada en:\n{path}")

    def load_key(self):
        path = filedialog.askopenfilename(filetypes=[("Archivo de clave", "*.key")])
        if path:
            with open(path, "rb") as f:
                self.key = f.read()
            if len(self.key) != 64:
                messagebox.showerror("Error", "La clave cargada no es válida.")
                self.key = None
            else:
                messagebox.showinfo("Clave cargada", "Clave cargada correctamente.")

    def encrypt_file(self):
        path = self.file_path.get()
        if not path:
            messagebox.showerror("Error", "Selecciona un archivo primero.")
            return

        try:
            if self.modo_cifrado.get() == "contraseña":
                contraseña, salt = self.solicitar_contraseña_con_salida()
                if not contraseña:
                    messagebox.showerror("Error", "No se ha introducido una contraseña válida.")
                    return
                self.key = self.derivar_clave_desde_contraseña(contraseña, salt)
                encryptor.encrypt_file(path, key=self.key, salt=salt, marker=b'VTXP')
            else:
                self.key = keygen.generate_random_key()
                encryptor.encrypt_file(path, key=self.key, marker=b'VTXK')
                key_path = path + ".key"
                with open(key_path, "wb") as f:
                    f.write(self.key)

            self.progress.set(1.0)
            resumen = f"""
✅ Cifrado completado

📄 Archivo original: {path}
🔐 Archivo cifrado: {path}.jvtex
🗝️ Clave {'derivada de contraseña' if self.modo_cifrado.get() == 'contraseña' else 'guardada en: ' + key_path}
"""
            messagebox.showinfo("Resumen de cifrado", resumen.strip())
            self.file_path.set("")
            self.progress.set(0)

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.progress.set(0)

    def decrypt_file(self):
        path = self.file_path.get()
        if not path:
            messagebox.showerror("Error", "Selecciona un archivo primero.")
            return

        try:
            with open(path, "rb") as f:
                marker = f.read(4)

                if marker == b'VTXP':
                    salt = f.read(16)
                    contraseña = self.pedir_contraseña()
                    if not contraseña:
                        messagebox.showerror("Error", "No se ha introducido una contraseña.")
                        return
                    self.key = self.derivar_clave_desde_contraseña(contraseña, salt)
                    encrypted_data = f.read()

                elif marker == b'VTXK':
                    if not self.key:
                        messagebox.showerror("Error", "No hay clave cargada.")
                        return
                    encrypted_data = f.read()

                else:
                    messagebox.showerror("Error", "Formato de archivo desconocido.")
                    return

            self.progress.set(0.5)
            decrypted = encryptor.vortex_decrypt(encrypted_data, self.key)

            # Generar nombre del archivo descifrado
            original_name = os.path.basename(path).replace(".jvtex", "")
            name_parts = original_name.rsplit(".", 1)

            if len(name_parts) == 2:
                output_name = f"{name_parts[0]}.dec.{name_parts[1]}"
            else:
                output_name = f"{original_name}.dec"

            output_path = os.path.join(os.path.dirname(path), output_name)

            with open(output_path, "wb") as out:
                out.write(decrypted)

            self.progress.set(1.0)
            messagebox.showinfo("Éxito", f"Archivo descifrado correctamente:\n{output_path}")
            self.file_path.set("")
            self.progress.set(0)

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.progress.set(0)

def launch_gui():
    root = TkinterDnD.Tk()
    root.attributes("-alpha", 0.0)  # Comienza totalmente transparente
    app = VortexApp(root)
    fade_in(root)  # Inicia la animación
    root.mainloop()
    
def fade_in(window, step=0.05, delay=30):
    alpha = window.attributes("-alpha")
    if alpha < 1.0:
        alpha = min(alpha + step, 1.0)
        window.attributes("-alpha", alpha)
        window.after(delay, lambda: fade_in(window, step, delay))


