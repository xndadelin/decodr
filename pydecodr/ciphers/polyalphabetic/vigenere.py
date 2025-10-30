"""
decodr.ciphers.polyalphabetic.vigenere - Vignere cipher

E_i = (P_i + K_i) mod 26
D_i = (C_i - K_i) mod 26
"""

from __future__ import annotations

def _shift(ch: str, k: int, decrypt: bool = False) -> str:
    if not ch.isalpha():
        return ch
    base = ord("A") if ch.isupper() else ord("a")
    offset = -k if decrypt else k
    return chr((ord(ch) - base + offset) % 26 + base)

def _key_shifts(key: str) -> list[int]:
    return [(ord(c.lower()) - ord("a")) for c in key if c.isalpha()]

def encrypt(plaintext: str, key: str) -> str:
    if not key:
        raise ValueError('Key cannot be empty')
    shifts = _key_shifts(key)
    out = []
    j = 0
    for ch in plaintext:
        if ch.isalpha():
            out.append(_shift(ch, shifts[j % len(shifts)]))
            j += 1
        else:
            out.append(ch)
    return "".join(out)

def decrypt(ciphertext: str, key: str) -> str:
    if not key:
        raise ValueError('Key cannot be empty')
    shifts = _key_shifts(key)
    out = []
    j = 0
    for ch in ciphertext:
        if ch.isalpha():
            out.append(_shift(ch, shifts[j % len(shifts)], decrypt=True))
            j += 1
        else:
            out.append(ch)
    return "".join(out)

encode = encrypt
decode = decrypt

if __name__ == "__main__":
    import sys

    usage = (
        "Usage:\n"
        "python3 -m decodr.ciphers.polyalphabetic.vigenere encrypt <text> <key>\n"
        "python3 -m decodr.ciphers.polyalphabetic.vigenere decrypt <text> <key>\n"
    )

    if len(sys.argv) < 4:
        print(usage)
        sys.exit(1)
    
    cmd, text, key = sys.argv[1:4]

    try:
        if cmd in("encrypt", "encode"):
            print(encrypt(text, key))
        elif cmd in ("decrypt", "decode"):
            print(decrypt(text, key))
        else:
            print("Unknown command. Use 'decrypt' or 'encrypt'.")
            print(usage)
    except Exception as e:
        print(f"Error {e}")
        sys.exit(1)

