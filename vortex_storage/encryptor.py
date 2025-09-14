# vortex_storage/encryptor.py

from vortex_core.cipher import vortex_encrypt, vortex_decrypt

def encrypt_file(path, key, salt=None, marker=b'VTXK'):
    with open(path, "rb") as f:
        data = f.read()

    encrypted_data = vortex_encrypt(data, key)

    output_path = path + ".jvtex"
    with open(output_path, "wb") as f:
        f.write(marker)  # 4 bytes para identificar el modo
        if salt:
            f.write(salt)  # 16 bytes si se usa contraseña
        f.write(encrypted_data)

def decrypt_file(path, key):
    with open(path, "rb") as f:
        marker = f.read(4)
        if marker == b'VTXP':
            salt = f.read(16)
            encrypted_data = f.read()
        elif marker == b'VTXK':
            encrypted_data = f.read()
        else:
            raise ValueError("Formato de archivo desconocido")

    return vortex_decrypt(encrypted_data, key)
