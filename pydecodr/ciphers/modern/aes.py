"""
pydecodr.ciphers.modern.aes - AES, CBC, PKCS7, with IV embedded
"""

from __future__ import annotations
import base64
from typing import Union
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import argparse
import sys

BLOCK_SIZE = 16

def _parse_key(key: Union[str, bytes], *, encoding: str = 'utf-8') -> bytes:
    if isinstance(key, bytes):
        k = key
    else:
        s = key
        if s.startswith("hex:"):
            try:
                k = bytes.fromhex(s[4:])
            except ValueError as e:
                raise ValueError("Invalid hex key after 'hex:' prefix")
        else:
            k = s.encode(encoding)
        
    if len(k) not in (16, 24, 32):
        raise ValueError("AES key must be 16, 24, or 32 bytes")
    return k

def encrypt(plaintext: str, key: Union[str, bytes], *, encoding: str = 'utf-8') -> str:
    k = _parse_key(key, encoding=encoding)
    iv = get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(k, AES.MODE_CBC, iv=iv)
    ct = cipher.encrypt(pad(plaintext.encode(encoding), BLOCK_SIZE))
    blob = iv + ct
    return base64.b64encode(blob).decode('ascii')

def decrypt(ciphertext_b64: str, key: Union[str, bytes], *, encoding: str = 'utf-8') -> str:
    k = _parse_key(key, encoding=encoding)
    try:
        blob = base64.b64decode(ciphertext_b64, validate=True)
    except Exception as e:
        raise ValueError("Ciphertext must be valid base64")
    
    if len(blob) < BLOCK_SIZE or (len(blob) - BLOCK_SIZE) % BLOCK_SIZE != 0:
        raise ValueError("invalid IV + ciphertext length")
    
    iv, ct = blob[:BLOCK_SIZE], blob[BLOCK_SIZE:]
    cipher = AES.new(k, AES.MODE_CBC, iv=iv)
    pt = unpad(cipher.decrypt(ct), BLOCK_SIZE)
    return pt.decode(encoding)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.modern.aes",
        description="AES-CBC with PKCS7 padding"
    )

    p.add_argument("action", choices=["encrypt", "decrypt"], help='action to perform')
    p.add_argument("data", help="plaintext (encrypt) or base64(iv||ciphertext) (decrypt)")
    p.add_argument("key", help="key bytes: literal text or 'hex:<hexstring>' (16/24/32 bytes)'")
    p.add_argument("--encoding", default="utf-8", help="text encoding for plaintext/key (default: utf-8)")

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
            sys.exit(9)
        elif action == "decrypt":
            print(decrypt(data, key, encoding=enc))
            sys.exit(0)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

        