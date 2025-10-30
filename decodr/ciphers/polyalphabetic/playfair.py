"""
decodrs.ciphers.polyalphabetic.playfair - playfair cipher (5x5, I/J merged)
"""

from __future__ import annotations
from typing import List, Tuple

ALPHABET_25 = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

def _normalize_key(key: str) -> str:
    seen = set()
    out = []
    for ch in key.upper():
        if not ch.isalpha():
            continue
        ch = "I" if ch == "J" else ch
        if ch not in seen and ch in ALPHABET_25:
            seen.add(ch)
            out.append(ch)
        
    return "".join(out)

def _build_square(key: str) -> List[List[str]]:
    norm = _normalize_key(key)
    rest = "".join(ch for ch in ALPHABET_25 if ch not in norm)
    seq = norm + rest
    return [list(seq[i: i + 5]) for i in range(0, 25, 5)]

def _pos(square: List[List[str]], ch: str) -> Tuple[int, int]:
    for r in range(5):
        for c in range(5):
            if square[r][c] == ch:
                return r, c
    raise ValueError(f"Letter {ch!r} not found in square")

def _prepare_text(text: str, pad: str = "X") -> List[Tuple[str, str]]:
    s = []
    for ch in text.upper():
        if ch.isalpha():
            s.append("I" if ch == "J" else ch)
    
    pairs: List[Tuple[str, str]] = []
    i = 0
    while i < len(s):
        a = s[i]
        b = s[i + 1] if i + 1 < len(s) else None
        if b is None:
            pairs.append((a, pad))
            i += 1
        elif a == b:
            pairs.append((a, pad))
            i += 1
        else:
            pairs.append((a, b))
            i += 2
    return pairs

def __process_pair(a: str, b: str, square: List[List[str]], decrypt: bool = False) -> Tuple[str, str]:
    ra, ca = _pos(square, a)
    rb, cb = _pos(square, b)

    if ra == rb:
        if decrypt:
            return square[ra][(ca - 1) % 5], square[rb][(cb - 1) % 5] 
        else:
            return square[ra][(ca + 1) % 5], square[rb][(cb + 1) % 5]
    
    if ca == cb:
        if decrypt:
            return square[(ra - 1) % 5][ca], square[(rb - 1) % 5][cb]
        else:
            return square[(ra + 1) % 5][ca], square[(rb + 1) % 5][cb]
    
    return square[ra][cb], square[rb][ca]

def encrypt(plaintext: str, key: str, pad: str = "X") -> str:
    square = _build_square(key)
    digrams = _prepare_text(plaintext, pad=pad)
    out: List[str] = []
    for a, b in digrams:
        ea, eb = __process_pair(a, b, square, decrypt=False)
        out.extend([ea, eb])
    
    return "".join(out)

def decrypt(ciphertext: str, key: str, pad: str = "X") -> str:
    square = _build_square(key)
    s = [("I" if ch == "J" else ch) for ch in ciphertext.upper() if ch.isalpha()]
    if len(s) % 2 != 0:
        raise ValueError("Ciphertext length must be even!")
    out: List[str] = []
    for i in range(0, len(s), 2):
        a, b = s[i], s[i + 1]
        da, db = __process_pair(a, b, square, decrypt=True)
        out.extend([da, db])

    return "".join(out)

encode = encrypt
decode = decrypt

if __name__ == "__main__":
    import sys
    usage = (
        "Usage:\n"
        "python3 -m decodr.ciphers.polyalphabetic.playfair encrypt <text> <key>\n"
        "python3 -m decodr.ciphers.polyalphabetic.playfair decrypt <text> <key>\n"
    )
    if len(sys.argv) < 4:
        print(usage)
        sys.exit(1)

    cmd, text, key = sys.argv[1:4]
    try:
        if cmd in ("encrypt", "encode"):
            print(encrypt(text, key))
        elif cmd in ("decrypt", "decode"):
            print(decrypt(text, key))
        else:
            print("Unknown command. Use 'encrypt' or 'decrypt'.")
            print(usage)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)