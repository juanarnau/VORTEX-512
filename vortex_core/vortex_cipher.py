# vortex_core/vortex_cipher.py
import os
import hmac
import hashlib
from vortex_core import keygen

BLOCK_SIZE = 64  # 512 bits

# 🔐 S-box derivada de la clave
def generate_sbox_from_key(key: bytes) -> list:
    seed = int.from_bytes(hashlib.sha256(key).digest(), 'big') % (2**32)
    rng = list(range(256))
    random = __import__('random')
    random.seed(seed)
    random.shuffle(rng)
    return rng

def generate_inverse_sbox(sbox: list) -> list:
    inverse = [0] * 256
    for i, val in enumerate(sbox):
        inverse[val] = i
    return inverse

def pad_data(data: bytes) -> bytes:
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len] * pad_len)

def unpad_data(data: bytes) -> bytes:
    pad_len = data[-1]
    if pad_len < 1 or pad_len > BLOCK_SIZE:
        raise ValueError("Relleno inválido")
    return data[:-pad_len]

def expand_key(master_key: bytes, rounds: int = 16) -> list:
    subkeys = []
    for i in range(rounds):
        rotated = master_key[i:] + master_key[:i]
        subkey = hashlib.sha512(rotated).digest()[:BLOCK_SIZE]
        subkeys.append(subkey)
    return subkeys

def sbox_substitution(block: bytes, sbox: list) -> bytes:
    return bytes([sbox[b] for b in block])

def inverse_sbox_substitution(block: bytes, inverse_sbox: list) -> bytes:
    return bytes([inverse_sbox[b] for b in block])

def permute_block(block: bytes) -> bytes:
    return block[::-1]

def inverse_permute_block(block: bytes) -> bytes:
    return block[::-1]

def vortex_round_encrypt(block: bytes, subkey: bytes, sbox: list) -> bytes:
    block = sbox_substitution(block, sbox)
    block = permute_block(block)
    block = bytes([b ^ k for b, k in zip(block, subkey)])
    return block

def vortex_round_decrypt(block: bytes, subkey: bytes, inverse_sbox: list) -> bytes:
    block = bytes([b ^ k for b, k in zip(block, subkey)])
    block = inverse_permute_block(block)
    block = inverse_sbox_substitution(block, inverse_sbox)
    return block

def generate_hmac(data: bytes, key: bytes) -> bytes:
    return hmac.new(key, data, hashlib.sha256).digest()

def vortex_encrypt_block(block: bytes, subkeys: list, sbox: list) -> bytes:
    for subkey in subkeys:
        block = vortex_round_encrypt(block, subkey, sbox)
    return block

def vortex_decrypt_block(block: bytes, subkeys: list, inverse_sbox: list) -> bytes:
    for subkey in reversed(subkeys):
        block = vortex_round_decrypt(block, subkey, inverse_sbox)
    return block

def vortex_encrypt(data: bytes, key: bytes, iv: bytes = None) -> bytes:
    data = pad_data(data)
    subkeys = expand_key(key)
    sbox = generate_sbox_from_key(key)
    if iv is None:
        iv = os.urandom(BLOCK_SIZE)
    encrypted = iv
    prev_block = iv

    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i+BLOCK_SIZE]
        block = bytes([b ^ p for b, p in zip(block, prev_block)])
        cipher_block = vortex_encrypt_block(block, subkeys, sbox)
        encrypted += cipher_block
        prev_block = cipher_block

    hmac_tag = generate_hmac(encrypted, key)
    return encrypted + hmac_tag

def vortex_decrypt(data: bytes, key: bytes) -> bytes:
    hmac_tag = data[-32:]
    encrypted_data = data[:-32]
    expected_hmac = generate_hmac(encrypted_data, key)
    if not hmac.compare_digest(hmac_tag, expected_hmac):
        raise ValueError("Autenticación fallida: los datos han sido modificados")

    subkeys = expand_key(key)
    sbox = generate_sbox_from_key(key)
    inverse_sbox = generate_inverse_sbox(sbox)
    iv = encrypted_data[:BLOCK_SIZE]
    encrypted_data = encrypted_data[BLOCK_SIZE:]
    decrypted = b''
    prev_block = iv

    for i in range(0, len(encrypted_data), BLOCK_SIZE):
        block = encrypted_data[i:i+BLOCK_SIZE]
        decrypted_block = vortex_decrypt_block(block, subkeys, inverse_sbox)
        decrypted_block = bytes([b ^ p for b, p in zip(decrypted_block, prev_block)])
        decrypted += decrypted_block
        prev_block = block

    return unpad_data(decrypted)