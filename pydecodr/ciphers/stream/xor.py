"""
pydecodr.ciphers.stream.xor - single-byte xor cipher
"""

from __future__ import annotations
from typing import Union
import sys
import argparse

def _parse_key_to_int(key: Union[int, str]) -> int:
    if isinstance(key, int):
        k = key
    else:
        s = key.strip().lower()
        k = int(s, 16) if s.startswith("0x") else int(s, 10)
    if not (0 <= k <= 255):
        raise ValueError("key must be from 0 to 255")
    return k

def _xor_single(data: bytes, k: int) -> bytes:
    return bytes(b ^ k for b in data)

def encrypt(plaintext: str, key: Union[int, str], *, encoding: str = "utf-8") -> str:
    k = _parse_key_to_int(key)
    pt = plaintext.encode(encoding)
    ct = _xor_single(pt, k)
    return ct.hex()

def decrypt(ciphertext_hex: str, key: Union[int, str], *, encoding: str = 'utf-8') -> str:
    k = _parse_key_to_int(key)
    try:
        ct = bytes.fromhex(ciphertext_hex)
    except ValueError as e:
        raise ValueError('ciphertext must be hex-encoded') from e
    pt = _xor_single(ct, k)
    return pt.decode(encoding, errors='strict')

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.stream.xor",
        description="XOR"
    )

    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument('data', help="plaintext (encrypt) or hex ciphertext (decrypt)")
    p.add_argument("key", help="XOR key (string)")
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
        elif action == "decrypt":
            print(decrypt(data, key, encoding=enc))
            sys.exit(0)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

        