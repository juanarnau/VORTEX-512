# vortex_core/cipher.py

from Crypto.Cipher import AES # type: ignore
from Crypto.Util.Padding import pad, unpad # type: ignore

def vortex_encrypt(data: bytes, key: bytes) -> bytes:
    cipher = AES.new(key[:32], AES.MODE_CBC)
    iv = cipher.iv
    encrypted = cipher.encrypt(pad(data, AES.block_size))
    return iv + encrypted

def vortex_decrypt(data: bytes, key: bytes) -> bytes:
    iv = data[:16]
    encrypted = data[16:]
    cipher = AES.new(key[:32], AES.MODE_CBC, iv=iv)
    return unpad(cipher.decrypt(encrypted), AES.block_size)
