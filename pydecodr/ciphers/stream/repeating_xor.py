"""
pydecodr.ciphers.stream.repeating_xor - repeating-key XOR cipher
"""

from __future__ import annotations
from typing import Union
import sys
import argparse

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

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.stream.repeating_xor",
        description="Repeating-key XOR"
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

        