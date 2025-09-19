import os

# Lista de funciones sospechosas (extraídas de vulture)
funciones_sospechosas = [
    "save_key",
    "load_key",
    "encrypt_folder",
    "vortex_round",
    "validate_input_file",
    "suggest_encrypted_name",
    "suggest_decrypted_name",
    "ensure_directory_exists",
    "prevent_overwrite",
    "app"  # aunque sea una variable, la incluimos por si acaso
]

# Ruta al repositorio
REPO_PATH = "VORTEX-512"

def buscar_uso(funcion, repo_path):
    resultados = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                ruta = os.path.join(root, file)
                try:
                    with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
                        for i, linea in enumerate(f, 1):
                            if funcion in linea and not linea.strip().startswith("def "):
                                resultados.append(f"{ruta} (línea {i}): {linea.strip()}")
                except Exception as e:
                    print(f"⚠️ Error leyendo {ruta}: {e}")
    return resultados

def main():
    for funcion in funciones_sospechosas:
        print(f"\n🔍 Buscando uso de: {funcion}")
        usos = buscar_uso(funcion, REPO_PATH)
        if usos:
            for uso in usos:
                print(f"  ✅ {uso}")
        else:
            print("  🚫 No se encontró uso en el proyecto.")

if __name__ == "__main__":
    main()