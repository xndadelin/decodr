"""
decodr.ciphers.classical.rot13 - ROT13 cipher via caesar(where shift is 13)
"""

from __future__ import annotations
from pydecodr.ciphers.classical import caesar

def encode(text: str) -> str:
    return caesar.encrypt(text, shift=13)

def decode(text: str) -> str:
    return caesar.decrypt(text, shift=13)

encrypt = encode
decrypt = decode

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python3 -m decodr.ciphers.classical.rot13 <encode|decode> <text>")
        sys.exit(1)
    
    cmd, text = sys.argv[1], sys.argv[2]

    try:
        if cmd in ("encode", "decode", "encrypt", "decrypt"):
            if cmd in ("encode", "encrypt"):
                print(encode(text))
            else:
                print(decode(text))
        else:
            print("Error: Unknown command. Use 'encode' or 'decode'.")
    except Exception as e:
        print(f"Error: {e}")