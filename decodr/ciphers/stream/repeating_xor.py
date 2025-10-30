"""
decodr.ciphers.stream.repeating_xor - repeating-key XOR cipher
"""

from __future__ import annotations
from typing import Union

def _key_to_bytes(key: Union[str, bytes], encoding: str = 'utf-8') -> bytes:
    if isinstance(key, bytes):
        return key
    if not key:
        raise ValueError("Key cannot be empty")
    return key.encode(encoding)

def _xor_repeat(data: bytes, key_bytes: bytes) -> bytes:
    klen = len(key_bytes)
    return bytes(data[i] ^ key_bytes[i % klen] for i in range(len(data)))

def encrypt(plaintext: str, key: Union[str, bytes], *, encoding: str = "utf-8") -> str:
    key_b = _key_to_bytes(key)
    pt = plaintext.encode(encoding)
    ct = _xor_repeat(pt, key_b)
    return ct.hex()

def decrypt(ciphertext_hex: str, key: Union[int, str], *, encoding: str = 'utf-8') -> str:
    key_b = _key_to_bytes(key)
    try:
        ct = bytes.fromhex(ciphertext_hex)
    except ValueError as e:
        raise ValueError('ciphertext must be hex-encoded') from e
    pt = _xor_repeat(ct, key_b)
    return pt.decode(encoding, errors='strict')

encode = encrypt
decode = decrypt

if __name__ == "__main__":
    import sys
    usage = (
        "Usage:\n"
        "python3 -m decodr.ciphers.stream.repeating_xor encrypt <text> <key> <encoding>\n"
        "python3 -m decodr.ciphers.stream.repeating_xor decrypt <hex> <key> <encoding>\n"
    )

    if len(sys.argv) < 4:
        print(usage)
        sys.exit(1)

    cmd, arg_text, key = sys.argv[1], sys.argv[2], sys.argv[3]
    enc = sys.argv[4] if len(sys.argv) >= 5 else 'utf-8'
    try:
        if cmd in ("encrypt", "encode"):
            print(encrypt(arg_text, key, encoding=enc))
        elif cmd in ("decrypt", "decode"):
            print(decrypt(arg_text, key, encoding=enc))
        else:
            print("Unknown command. Use 'encrypt' or 'decrypt'.")
            print(usage)
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)