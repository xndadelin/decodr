"""
decodr.ciphers.classical.caesar - Caesar cipher - a monoalphabetic shift

Features:
- encrypt or decript using a integer shift
- non-letters are gonna be preserved as is
"""

from __future__ import annotations

def _shift_char(ch: str, shift: int) -> str:
    if "a" <= ch <= "z":
        base = ord("a")
        return chr((ord(ch) - base + shift) % 26 + base)
    if "A" <= ch <= "Z":
        base = ord("A")
        return chr((ord(ch) - base + shift) % 26 + base)
    return ch

def encrypt(plaintext: str, shift: int = 3) -> str:
    s = shift % 26
    return "".join(_shift_char(ch, s) for ch in plaintext)

def decrypt(ciphertext: str, shift: int = 3) -> str:
    s = (-shift)%26
    return "".join(_shift_char(ch, s) for ch in ciphertext)

def encode(text: str, shift: int = 3) -> str:
    return encrypt(text, shift=shift)

def decode(text: str, shift: int = 3) -> str:
    return decrypt(text, shift=shift)
    
def crack(ciphertext: str) -> list[tuple[int, str]]:
    results: list[tuple[int, str]] = []
    for sh in range(26):
        pt = decrypt(ciphertext, shift=sh)
        results.append((sh, pt))
    return results

if __name__ == "__main__":
    import sys
    usage = (
        "Usage:\n"
        "python3 -m decodr.ciphers.classical.caesar encrypt <text> [shift]\n"
        "python3 -m decodr.ciphers.classical.caesar decrypt <text> [shift]\n"
        "python3 -m decodr.ciphers.classical.caesar crack <text>\n"
    )
    if(len(sys.argv) < 3):
        print(usage)
        sys.exit(1)
    
    cmd = sys.argv[1]
    text = sys.argv[2]
    shift = int(sys.argv[3]) if len(sys.argv) >= 4 else 3

    try:
        if cmd == "encrypt":
            print(encrypt(text, shift=shift))
        elif cmd == "decrypt":
            print(decrypt(text, shift=shift))
        elif cmd == "crack":
            for sh, pt in crack(text):
                print(f"{sh:2d}: {pt}")
        else:
            print("Error: Unknown command. Use 'encrypt', 'decrypt' or 'crack'.")
            print(usage)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

