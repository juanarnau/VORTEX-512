# vortex_core/vortex_cipher.py

import os
import hashlib
from vortex_core import keygen

BLOCK_SIZE = 64  # 512 bits

def pad_data(data: bytes) -> bytes:
    """Relleno PKCS7 para bloques de 64 bytes."""
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len] * pad_len)

def unpad_data(data: bytes) -> bytes:
    """Elimina el relleno PKCS7."""
    pad_len = data[-1]
    if pad_len < 1 or pad_len > BLOCK_SIZE:
        raise ValueError("Relleno inválido")
    return data[:-pad_len]

def expand_key(master_key: bytes, rounds: int = 16) -> list:
    """Genera subclaves para cada ronda."""
    subkeys = []
    for i in range(rounds):
        rotated = master_key[i:] + master_key[:i]
        subkey = hashlib.sha512(rotated).digest()[:BLOCK_SIZE]
        subkeys.append(subkey)
    return subkeys

def sbox_substitution(block: bytes) -> bytes:
    """Aplica sustitución usando una S-box simple."""
    sbox = [(i * 73) % 256 for i in range(256)]
    return bytes([sbox[b] for b in block])

def permute_block(block: bytes) -> bytes:
    """Permuta los bytes del bloque (inversión simple)."""
    return block[::-1]

def vortex_round(block: bytes, subkey: bytes) -> bytes:
    block = sbox_substitution(block)
    block = permute_block(block)
    block = bytes([b ^ k for b, k in zip(block, subkey)])
    return block

def vortex_encrypt_block(block: bytes, subkeys: list) -> bytes:
    for subkey in subkeys:
        block = vortex_round_encrypt(block, subkey)
    return block

def vortex_decrypt_block(block: bytes, subkeys: list) -> bytes:
    for subkey in reversed(subkeys):
        block = vortex_round_decrypt(block, subkey)
    return block

def vortex_encrypt(data: bytes, key: bytes, iv: bytes = None) -> bytes:
    """Cifra datos completos en modo CBC."""
    data = pad_data(data)
    subkeys = expand_key(key)
    if iv is None:
        iv = os.urandom(BLOCK_SIZE)
    encrypted = iv
    prev_block = iv

    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i+BLOCK_SIZE]
        block = bytes([b ^ p for b, p in zip(block, prev_block)])  # XOR con bloque anterior
        cipher_block = vortex_encrypt_block(block, subkeys)
        encrypted += cipher_block
        prev_block = cipher_block

    return encrypted

def vortex_decrypt(data: bytes, key: bytes) -> bytes:
    """Descifra datos completos en modo CBC."""
    subkeys = expand_key(key)
    iv = data[:BLOCK_SIZE]
    data = data[BLOCK_SIZE:]
    decrypted = b''
    prev_block = iv

    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i+BLOCK_SIZE]
        decrypted_block = vortex_decrypt_block(block, subkeys)
        decrypted_block = bytes([b ^ p for b, p in zip(decrypted_block, prev_block)])
        decrypted += decrypted_block
        prev_block = block

    return unpad_data(decrypted)
def inverse_sbox_substitution(block: bytes) -> bytes:
    """Aplica la sustitución inversa usando la S-box invertida."""
    sbox = [(i * 73) % 256 for i in range(256)]
    inverse_sbox = [0] * 256
    for i, val in enumerate(sbox):
        inverse_sbox[val] = i
    return bytes([inverse_sbox[b] for b in block])

def inverse_permute_block(block: bytes) -> bytes:
    """Inversión de la permutación (en este caso, igual que la original)."""
    return block[::-1]

def vortex_round_encrypt(block: bytes, subkey: bytes) -> bytes:
    block = sbox_substitution(block)
    block = permute_block(block)
    block = bytes([b ^ k for b, k in zip(block, subkey)])
    return block

def vortex_round_decrypt(block: bytes, subkey: bytes) -> bytes:
    block = bytes([b ^ k for b, k in zip(block, subkey)])
    block = inverse_permute_block(block)
    block = inverse_sbox_substitution(block)
    return block