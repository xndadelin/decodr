"""
decodr.encodings.hex_mod - Hexadecimal encode/decode helpers

Supports:
- encoding UTF-8 text to hex
- decoding hex strings 
"""

from __future__ import annotations
import binascii

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


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python3 -m decodr.encodings.hex_mod <encode|decode> <text>")
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