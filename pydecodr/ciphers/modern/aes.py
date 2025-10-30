"""
decodr.ciphers.modern.aes - AES, CBC, PKCS7, with IV embedded
"""

from __future__ import annotations
import base64
from typing import Union
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

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

encode = encrypt
decode = decrypt

if __name__ == "__main__":
    import sys

    usage = (
        "Usage:\n"
        "python3 -m decodr.ciphers.modern.aes encrypt <text> <key>\n"
        "python3 -m decodr.ciphers.moder.aes decrypt <base64_iv_plus_ct> <key>\n"
    )

    if len(sys.argv) < 4:
        print(usage)
        sys.exit(1)

    cmd, arg1, key = sys.argv[1], sys.argv[2], sys.argv[3]
    try:
        if cmd in ("encrypt", "encode"):
            print(encrypt(arg1, key))
        elif cmd in ("decrypt", "decode"):
            print(decrypt(arg1, key))
        else:
            print("Unknown command. Use 'encrypt' or 'decrypt'.")
            print(usage)
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)