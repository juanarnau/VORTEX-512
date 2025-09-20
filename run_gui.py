import customtkinter as ctk
from tkinterdnd2 import TkinterDnD
from vortex_gui.gui import VortexApp
import tkinter as tk
from PIL import Image, ImageTk
import os
import sys
import ctypes
from utils import resource_path

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("vortex512.juanarnau.suite")

class DnDApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("VORTEX-512")
        self.geometry("700x500")
        self.configure(bg="#0a1f44")  # Fondo oscuro manual


def show_splash(root):
    splash = ctk.CTkToplevel(root)
    splash.geometry("500x300")
    splash.overrideredirect(True)
    splash.configure(fg_color="#0a1f44")
    splash.attributes("-alpha", 0.0)
    #splash.iconbitmap(resource_path("docs/assets/vortex.ico"))  # Aplica el ícono también al splash
    # Ruta al logo
    logo_path = os.path.join("docs", "assets", "logo.png")

    try:
        image = Image.open(resource_path("docs/assets/logo.png"))
        image = image.resize((100, 100))  # Ajusta el tamaño según tu diseño
        logo = ImageTk.PhotoImage(image)

        logo_label = tk.Label(splash, image=logo, bg="#0a1f44")
        logo_label.image = logo  # Evita que el recolector de basura lo elimine
        logo_label.pack(pady=(30, 10))
    except Exception as e:
        print(f"No se pudo cargar el logo: {e}")

    ctk.CTkLabel(splash, text="Zyphrix-512", font=("Segoe UI", 28, "bold"), text_color="white").pack(pady=(10, 5))
    ctk.CTkLabel(splash, text="Protegiendo tus datos desde el núcleo", font=("Segoe UI", 16), text_color="#cccccc").pack()
    # Copyright debajo
    tk.Label(splash, text="© Juan Arnau 2025", font=("Segoe UI", 10), fg="#cccccc", bg="#0a1f44").pack(pady=(20, 5))

    def fade_in():
        alpha = splash.attributes("-alpha")
        if alpha < 1.0:
            splash.attributes("-alpha", alpha + 0.05)
            splash.after(30, fade_in)

    def fade_in():
        alpha = splash.attributes("-alpha")
        if alpha < 1.0:
            splash.attributes("-alpha", alpha + 0.05)
            splash.after(30, fade_in)

    def launch_main():
        splash.destroy()
        root.deiconify()

    fade_in()
    root.after(3000, launch_main)

def launch_gui():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root = DnDApp()
    root.withdraw()  # Oculta la ventana principal
    root.iconbitmap(resource_path("docs/assets/vortex.ico"))    # Aplica el ícono antes de mostrar

    show_splash(root)  # Muestra el splash

    app = VortexApp(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()