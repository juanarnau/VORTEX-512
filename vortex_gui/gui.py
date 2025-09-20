import customtkinter as ctk
from tkinter import filedialog
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
from CTkMessagebox import CTkMessagebox
from vortex.file_crypto import encrypt_file, decrypt_file
from vortex.folder_crypto import encrypt_folder, decrypt_folder
from PIL import Image, ImageTk
import os
import tkinter as tk
from utils import resource_path  
from vortex_core import vortex_cipher
from vortex.folder_crypto import encrypt_folder
from vortex.folder_crypto import decrypt_folder

class VortexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zipherion-512 Encryption Suite")
        self.root.geometry("600x400")
        self.build_interface()
        try:
            self.root.iconbitmap(resource_path("docs/assets/logo.ico"))
        except:
            pass

    def build_interface(self):
        # Contenedor principal
        main_container = tk.Frame(self.root, bg="#0a1f44")
        main_container.pack(expand=True, fill="both")

        # Frame izquierdo para el logo y texto
        logo_frame = tk.Frame(main_container, bg="#0a1f44")
        logo_frame.pack(side="left", fill="y", padx=10, pady=10)
        # Cargar imagen del logo
        try:
            logo_path = resource_path("docs/assets/logo.png")
            image = Image.open(logo_path)
            image = image.resize((80, 80))
            logo = ImageTk.PhotoImage(image)
            logo_label = tk.Label(logo_frame, image=logo, bg="#0a1f44")
            logo_label.image = logo
            logo_label.pack(pady=(20, 5))
        except Exception as e:
            print(f"Error al cargar logo: {e}")

        # Texto debajo del logo
        text_label = tk.Label(logo_frame, text="Zipherion-512", font=("Segoe UI", 14, "bold"), fg="white", bg="#0a1f44")
        text_label.pack()

        # Frame derecho para la interfaz principal
        content_frame = ctk.CTkFrame(main_container)
        content_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        tabview = ctk.CTkTabview(content_frame)
        tabview.pack(expand=True, fill="both", padx=20, pady=20)

        # Pestaña Archivos
        tab_archivos = tabview.add("Archivos")
        ctk.CTkButton(tab_archivos, text="🔐 Cifrar archivo", command=self.cifrar_archivo).pack(pady=10)
        ctk.CTkButton(tab_archivos, text="🔓 Descifrar archivo", command=self.descifrar_archivo).pack(pady=10)

        # Pestaña Carpetas
        tab_carpetas = tabview.add("Carpetas")
        ctk.CTkButton(tab_carpetas, text="📁 Cifrar carpeta", command=self.cifrar_carpeta).pack(pady=10)
        ctk.CTkButton(tab_carpetas, text="📂 Descifrar carpeta", command=self.descifrar_carpeta).pack(pady=10)

        # Botón de salida
        ctk.CTkButton(content_frame, text="❌ Salir", command=self.root.quit).pack(pady=5)
       # Texto de copyright en la parte inferior
        anchor_label = tk.Label(
            content_frame,
            text="© Juan Arnau 2025",
            font=("Segoe UI", 10, "italic"),
            fg="#cccccc",
            bg="#0a1f44"
        )
        anchor_label.pack(side="bottom", pady=(10, 5), anchor="center")

    # Métodos para archivos
    def cifrar_archivo(self):
        file_path = filedialog.askopenfilename(title="Selecciona archivo a cifrar")
        if not file_path:
            return
        password = self.obtener_contraseña_confirmada()
        if not password:
            return
        try:
            key = self.derive_key_from_password(password)
            with open(file_path, "rb") as f:
                data = f.read()
            encrypted = vortex_cipher.vortex_encrypt(data, key)
            output_path = file_path + ".vortex"
            with open(output_path, "wb") as f:
                f.write(encrypted)
            CTkMessagebox(
                title="✅ Archivo cifrado",
                message=f"Archivo cifrado correctamente:\n{os.path.basename(output_path)}",
                icon="check"
            )
        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Error al cifrar archivo:\n{str(e)}",
                icon="cancel"
            )

    def descifrar_archivo(self):
        file_path = filedialog.askopenfilename(title="Selecciona archivo cifrado")
        if not file_path:
            return

        password = self.obtener_contraseña()
        if not password:
            print("Contraseña no válida o cancelada")
            return

        try:
            key = self.derive_key_from_password(password)
            with open(file_path, "rb") as f:
                encrypted_data = f.read()

            try:
                decrypted = vortex_cipher.vortex_decrypt(encrypted_data, key)
                output_path = file_path.replace(".vortex", "")
                with open(output_path, "wb") as f:
                    f.write(decrypted)

                CTkMessagebox(
                    title="✅ Autenticidad confirmada",
                    message="El archivo es legítimo y ha sido descifrado correctamente.",
                    icon="check"
                )
            except ValueError:
                CTkMessagebox(
                    title="❌ Autenticidad fallida",
                    message="El archivo ha sido modificado o no es válido. Descifrado bloqueado.",
                    icon="cancel"
                )

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Error inesperado:\n{str(e)}",
                icon="cancel"
            )

    # Métodos para carpetas
    def cifrar_carpeta(self):
        folder_path = filedialog.askdirectory(title="Selecciona carpeta a cifrar")
        if not folder_path:
            return
        password = self.obtener_contraseña_confirmada()
        if not password:
            return
        try:
            key = self.derive_key_from_password(password)
            archivos_cifrados = encrypt_folder(folder_path, key)
            if archivos_cifrados > 0:
                CTkMessagebox(
                    title="Éxito",
                    message=f"{archivos_cifrados} archivos cifrados correctamente",
                    icon="check"
                )
            else:
                CTkMessagebox(
                    title="Aviso",
                    message="No se encontraron archivos para cifrar",
                    icon="info"
                )
        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Error al cifrar carpeta:\n{str(e)}",
                icon="cancel"
            )
    def descifrar_carpeta(self):
        folder_path = filedialog.askdirectory(title="Selecciona carpeta cifrada")
        if not folder_path:
            return
        password = self.obtener_contraseña()
        if not password:
            return
        try:
            key = self.derive_key_from_password(password)
            archivos = decrypt_folder(folder_path, key)
            if archivos > 0:
                CTkMessagebox(title="Éxito", message=f"{archivos} archivos descifrados correctamente", icon="check")
            else:
                CTkMessagebox(title="Aviso", message="No se encontraron archivos cifrados", icon="info")
        except ValueError as ve:
            CTkMessagebox(title="Error", message=str(ve), icon="cancel")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Descifrado fallido:\n{str(e)}", icon="cancel")

    # Validación de contraseña doble
    def obtener_contraseña_confirmada(self):
        dialog1 = ctk.CTkInputDialog(text="Introduce tu contraseña", title="Cifrado por contraseña")
        password1 = dialog1.get_input()

        dialog2 = ctk.CTkInputDialog(text="Confirma tu contraseña", title="Confirmación")
        password2 = dialog2.get_input()

        if password1 and password2 and password1 == password2:
            return password1
        else:
            ctk.CTkMessagebox(title="Error", message="Las contraseñas no coinciden", icon="cancel")
            return None


    # Solo pedir una vez (para descifrado)
    def obtener_contraseña(self):
        dialog = ctk.CTkInputDialog(text="Introduce tu contraseña", title="Descifrado")
        return dialog.get_input()

    # Derivar clave desde contraseña
    def derive_key_from_password(self, password):
        salt = b"vortex_salt"  # Puedes hacerlo dinámico si quieres
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))