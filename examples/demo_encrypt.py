from vortex_core import keygen
from vortex_storage import encryptor

key = keygen.generate_random_key()

# Cifrar
encryptor.encrypt_file("mensaje.txt", key=key)

# Descifrar
encryptor.decrypt_file("mensaje.txt.jvtex", key=key)