"""
decodr.ciphers.stream.xor - single-byte xor cipher
"""

from __future__ import annotations
from typing import Union

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

encode = encrypt
decode = decrypt

if __name__ == "__main__":
    import sys
    usage = (
        "Usage:\n"
        "python3 -m decodr.ciphers.stream.xor encrypt <text> <key> <encoding>\n"
        "python3 -m decodr.ciphers.stream.xor decrypt <hex> <key> <encoding>\n"
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