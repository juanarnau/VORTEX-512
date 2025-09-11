# -*- coding: utf-8 -*-
import customtkinter
from file_ops import (
    cifrar_archivo,
    descifrar_archivo,
    cifrar_carpeta,
    descifrar_carpeta
)

customtkinter.set_appearance_mode("dark")  # Opciones: "light", "dark", "system"
customtkinter.set_default_color_theme("blue")  # Opciones: "blue", "green", "dark-blue"

def iniciar_ventana_principal(root):
    root.deiconify()
    root.geometry("500x450")
    root.title("🛡️ VORTEX-512 Total Security")

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    customtkinter.CTkLabel(frame, text="Suite de cifrado de archivos y carpetas", font=("Arial", 16, "bold")).pack(pady=10)

    customtkinter.CTkButton(frame, text="📄 Cifrar archivo", command=cifrar_archivo, width=240).pack(pady=5)
    customtkinter.CTkButton(frame, text="📁 Cifrar carpeta", command=cifrar_carpeta, width=240).pack(pady=5)
    customtkinter.CTkButton(frame, text="🔓 Descifrar archivo", command=descifrar_archivo, width=240).pack(pady=5)
    customtkinter.CTkButton(frame, text="🔓 Descifrar carpeta", command=descifrar_carpeta, width=240).pack(pady=5)

    customtkinter.CTkLabel(frame, text="Extensión personalizada: .jvsec", font=("Arial", 12)).pack(pady=10)
    customtkinter.CTkLabel(frame, text="Creado por Juan · VORTEX-512", font=("Arial", 12)).pack(pady=5)