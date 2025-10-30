"""
decodr.encodings.base32_mod - Base32 encode/decode helpers.

Features:
- UTF-8 text in/out (internal bytes conversion)
- based on https://datatracker.ietf.org/doc/html/rfc4648
- do not worry about missing padding on decode
"""

from __future__ import annotations
import base64


def _to_bytes(s: str) -> bytes:
    return s.encode('utf-8')

def _to_str(b: bytes) -> str:
    return b.decode('utf-8', errors="ignore")

def _fix_padding(s: str) -> str:
    r = len(s) % 8
    return s if r == 0 else s + ('=' * (8 - r))

def encode(text: str, *, padding: bool = True) -> str:
    raw = _to_bytes(text)
    out = base64.b32encode(raw).decode("ascii")
    return out if padding else out.rstrip("=")

def decode(b64text: str, *, strict: bool = False) -> str:
    data = b64text.strip().replace("\n", "").replace("\r", "").replace(" ", "")
    if not strict:
        data = _fix_padding(data)

    try: 
        decoded = base64.b32decode(data, casefold=True)
    except Exception as e:
        raise ValueError(f"Invalid base34 input: {e}") from e
    
    return _to_str(decoded)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python3 -m decodr.encodings.base32_mod <encode|decode> <text>")
        sys.exit(1)

    cmd, text = sys.argv[1], sys.argv[2]

    try:
        if cmd == 'encode':
            print(encode(text))
        elif cmd == "decode":
            print(decode(text))
        else:
            print("Error: Unknown command. Use 'encode' or 'decode'.")
    except Exception as e:
        print(f"Error: {e}")