import hashlib

def expand_key(master_key, rounds):
    subkeys = []
    for i in range(rounds):
        data = master_key + i.to_bytes(2, 'big')
        subkey = hashlib.sha3_256(data).digest()
        subkeys.append(subkey)
    return subkeys

def substitution(block, subkey):
    return bytes([(b ^ subkey[i % len(subkey)]) for i, b in enumerate(block)])

def permutation(block):
    return block[::-1]

def vortex_encrypt(data, key, block_size=32, rounds=10):
    subkeys = expand_key(key, rounds)
    padding_len = block_size - (len(data) % block_size)
    data += bytes([padding_len]) * padding_len
    blocks = [data[i:i+block_size] for i in range(0, len(data), block_size)]
    encrypted = []
    for block in blocks:
        state = block
        for i in range(rounds):
            state = substitution(state, subkeys[i])
            state = permutation(state)
        encrypted.append(state)
    return b''.join(encrypted)

def vortex_decrypt(data, key, block_size=32, rounds=10):
    subkeys = expand_key(key, rounds)
    blocks = [data[i:i+block_size] for i in range(0, len(data), block_size)]
    decrypted = []
    for block in blocks:
        state = block
        for i in reversed(range(rounds)):
            state = permutation(state)
            state = substitution(state, subkeys[i])
        decrypted.append(state)
    data = b''.join(decrypted)
    padding_len = data[-1]
    return data[:-padding_len]# -*- coding: utf-8 -*-

