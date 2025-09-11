# -*- coding: utf-8 -*-
import customtkinter
from PIL import Image, ImageTk

def mostrar_splash(root):
    splash = customtkinter.CTkToplevel(root)
    splash.overrideredirect(True)
    splash.geometry("400x420+500+200")
    splash.configure(fg_color="#0a1f3d")

    try:
        img = Image.open("vortex_logo.png").resize((200, 200))
        logo = ImageTk.PhotoImage(img)
        splash.logo = logo  # Mantener referencia

        customtkinter.CTkLabel(splash, image=logo, text="", fg_color="#0a1f3d").pack(pady=30)
    except Exception:
        customtkinter.CTkLabel(splash, text="VORTEX-512", font=("Arial", 20, "bold"), text_color="white", fg_color="#0a1f3d").pack(pady=30)

    customtkinter.CTkLabel(splash, text="Bienvenido a VORTEX-512", font=("Arial", 14, "bold"), text_color="white", fg_color="#0a1f3d").pack()
    customtkinter.CTkLabel(splash, text="Protegiendo tus datos desde el núcleo", font=("Arial", 10), text_color="#80cfff", fg_color="#0a1f3d").pack(pady=5)

    splash.after(3000, splash.destroy)