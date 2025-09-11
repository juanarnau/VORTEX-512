# -*- coding: utf-8 -*-
import tkinter as tk
from splash import mostrar_splash
from ui import iniciar_ventana_principal

def main():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal temporalmente

    mostrar_splash(root)  # Muestra el splash
    root.after(3100, lambda: iniciar_ventana_principal(root))  # Muestra la interfaz principal

    root.mainloop()

if __name__ == "__main__":
    main()
