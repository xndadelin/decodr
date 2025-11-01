"""
pydecodr.encodings.hex_mod - Hexadecimal encode/decode helpers

Supports:
- encoding UTF-8 text to hex
- decoding hex strings 
"""

from __future__ import annotations
import binascii
import sys
import argparse

def _to_bytes(s: str) -> bytes:
    return s.encode('utf-8')

def _to_str(b: bytes) -> str:
    return b.decode('utf-8', errors="ignore")

def encode(text: str, uppercase: bool = False, spaced: bool = False) -> str:
    raw = _to_bytes(text)
    hex = binascii.hexlify(raw).decode('ascii')
    if uppercase:
        hex = hex.upper()
    if spaced:
        hex = " ".join(hex[i:i+2] for i in range (0, len(hex), 2)) 
    
    return hex

def decode(hextext: str, strict: bool = True) -> str:
    data = hextext.strip().replace(" ", "").replace("\n", "").replace("\r", "")

    try:
        decoded = binascii.unhexlify(data)
    except Exception as e:
        if strict:
            raise ValueError(f"Error: Invalid hex input: {e}") from e
        else:
            cleaned = "".join(ch for ch in data if ch.lower() in "0123456789abcdef")
            decoded = binascii.unhexlify(cleaned)
    return _to_str(decoded)


def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.encodings.hex_mod",
        description="Hex encoding/decoding utility"
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