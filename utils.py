import os
import sys

def resource_path(relative_path):
    """Devuelve la ruta absoluta al recurso, compatible con PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)
