"""
decodr.ciphers.stream.rc4 - RC4 stream cipher
"""

from __future__ import annotations
from typing import Union, List, Generator

def _ksa(key_bytes: bytes) -> List[int]:
    key_length = len(key_bytes)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key_bytes[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]

    return S

def _prga(S: List[int]) -> Generator[int, None, None]:
    i, j = 0, 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K

def _rc4_encrypt(data: bytes, key_bytes: bytes) -> bytes:
    S = _ksa(key_bytes)
    keystream = _prga(S)
    return bytes(b ^ next(keystream) for b in data)

def encrypt(plaintext: str, key: Union[str, bytes], *, encoding: str = 'utf-8') -> str:
    key_b = key.encode(encoding) if isinstance(key, str) else key
    if not key_b:
        raise ValueError("Key cannot be empty.")

    pt = plaintext.encode(encoding)
    ct = _rc4_encrypt(pt, key_b)
    return ct.hex()

def decrypt(ciphertext_hex: str, key: Union[str, bytes], *, encoding: str = 'utf-8') -> str:
    key_b = key.encode(encoding) if isinstance(key, str) else key
    if not key_b:
        raise ValueError("Key cannot be empty.")
    try:
        ct = bytes.fromhex(ciphertext_hex)
    except ValueError as e:
        raise ValueError("Ciphertext must be hex-encoded") from e
    pt = _rc4_encrypt(ct, key_b)
    return pt.decode(encoding, errors='strict')

encode = encrypt
decode = decrypt


if __name__ == "__main__":
    import sys
    usage = (
        "Usage:\n"
        "python3 -m decodr.ciphers.stream.rc4 encrypt <text> <key> <encoding>\n"
        "python3 -m decodr.ciphers.stream.rc4 decrypt <hex>  <key> <encoding>\n"
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