"""
pydecodr.encodings.base32_mod - Base32 encode/decode helpers.

Features:
- UTF-8 text in/out (internal bytes conversion)
- based on https://datatracker.ietf.org/doc/html/rfc4648
- do not worry about missing padding on decode
"""

from __future__ import annotations
import base64
import sys
import argparse


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

def decode(b32text: str, *, strict: bool = False) -> str:
    data = b32text.strip().replace("\n", "").replace("\r", "").replace(" ", "")
    if not strict:
        data = _fix_padding(data)

    try: 
        decoded = base64.b32decode(data, casefold=True)
    except Exception as e:
        raise ValueError(f"Invalid base34 input: {e}") from e
    
    return _to_str(decoded)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.encodings.base32_mod",
        description="Base32 encoding/decoding utility"
    )

    p.add_argument("action", choices=["encode", "decode"], help="action to perform")
    p.add_argument("text", help="text to encode or decode (quote if contains spaces)")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    action = args.action
    text = args.text

    try:
        if action == "encode":
            print(encode(text))
            sys.exit(0)
        elif action == "decode":
            print(decode(text))
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)