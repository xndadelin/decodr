"""
decodr.ciphers.classical.atbash - Atbash cipher

Basically each letter is mapped to its reverse counterpard:
A <-> Z, B <-> Y ...
"""

from __future__ import annotations

def _map_char(ch: str) -> str:
    if "a" <= ch <= "z":
        return chr(ord("z") - (ord(ch) - ord("a")))
    if "A" <= ch <= "Z":
        return chr(ord("Z") - (ord(ch) - ord("A")))
    return ch

def transform(text: str) -> str:
    return "".join(_map_char(ch) for ch in text)

def encode(text: str) -> str:
    return transform(text)

decode = encode
encrypt = encode
decrypt = decode

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python3 -m decodr.ciphers.classical.atbash <encode|decode> <text>")
        sys.exit(1)
    
    cmd, text = sys.argv[1], sys.argv[2]
    try:
        if cmd in ("encode", "decode", "encrypt", "decrypt"):
            print(transform(text))
        else:
            print("Error: Unknown command. Use 'encode' or 'decode'.")
    except Exception as e:
        print(f"Error: {e}")

