"""
pydecodr.ciphers.stream.rc4 - RC4 stream cipher
"""

from __future__ import annotations
from typing import Union, List, Generator
import sys
import argparse

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

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.stream.rc4",
        description="RC4 stream cipher"
    )
    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("data", help="plaintext (encrypt) or hex ciphertex (decrypt)")
    p.add_argument("key", help="key for RC4 (string)")
    p.add_argument("--encoding", default="utf-8", help="text encoding (default: utf-8)")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    action = args.action
    data = args.data
    key = args.key
    enc = args.encoding

    try:
        if action == "encrypt":
            print(encrypt(data, key, encoding=enc))
            sys.exit(0)
        elif action == 'decrypt':
            print(decrypt(data, key, encoding=enc))
            sys.exit(0)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
        