"""
pydecodr.ciphers.fractionation.trifid - trifid ciphers (3x3x3, A-Z + '+')
"""

from __future__ import annotations
import sys
import argparse 

ALPH27 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ+"
ALLOWED_FOR_KEY = set(ALPH27)

# to do, fix the meta cases

def _build_keyed_alphabet(key: str) -> str:
    k = "".join(ch for ch in key.upper() if ch in ALLOWED_FOR_KEY)
    seen = set()
    out = []
    for ch in k + ALPH27:
        if ch not in seen:
            seen.add(ch)
            out.append(ch)
    return "".join(out)

def _coords(idx: int) -> tuple[int, int, int]:
    z = idx // 9
    rem = idx % 9
    r = rem // 3
    c = rem % 3
    return z, r, c

def _index(z: int, r: int, c: int) -> int:
    return z * 9 + r * 3 + c

def _letters_and_meta(s: str) -> tuple[list[str], list[tuple[int, str]]]:
    letters = []
    meta = []
    for i, ch in enumerate(s):
        if "A" <= ch <= "Z":
            letters.append(ch)
            meta.append((i, "upper"))
        elif "a" <= ch <= "z":
            letters.append(ch.upper())
            meta.append((i, "lower"))
        elif ch == "+":
            letters.append("+")
            meta.append((i, "upper"))
        else:
            meta.append((i, "non"))
    return letters, meta

def _reinject(original: str, seq: list[str], meta: list[tuple[int, str]]) -> str:
    res = list(original)
    it = iter(seq)
    for i, ch in enumerate(original):
        if "A" <= ch <= "Z":
            nxt = next(it, None)
            if nxt is None: 
                break
            res[i] = nxt
        elif "a" <= ch <= "z":
            nxt = next(it, None)
            if nxt is None: 
                break
            res[i] = nxt.lower()
        elif ch == "+":
            nxt = next(it, None)
            if nxt is None: 
                break
            res[i] = nxt
        else:
            pass
    return "".join(res)

def encrypt(plaintext: str, key: str = "", period: int = 5) -> str:
    period = int(period)
    if period <= 0:
        raise ValueError("period must be >=1")
    alpha = _build_keyed_alphabet(key)
    idx = {c: i for i, c in enumerate(alpha)}

    letters, meta = _letters_and_meta(plaintext)
    if not letters:
        return plaintext

    out_letters: list[str] = []
    i = 0
    n = len(letters)
    while i < n:
        block = letters[i:i+period]
        Z, R, C = [], [], []
        for ch in block:
            j = idx[ch]
            z, r, c = _coords(j)
            Z.append(z)
            R.append(r)
            C.append(c)
        m = len(block)
        flat = Z + R + C
        for t in range(0, 3*m, 3):
            z, r, c = flat[t], flat[t+1], flat[t+2]
            out_letters.append(alpha[_index(z, r, c)])
        i += period
    
    return _reinject(plaintext, out_letters, meta)

def decrypt(ciphertext: str, key: str = "", period: int = 5) -> str:
    period = int(period)
    if period <= 0:
        raise ValueError("period must be >=1")
    alpha = _build_keyed_alphabet(key)
    idx = {c: i for i, c in enumerate(alpha)}

    letters, meta = _letters_and_meta(ciphertext)
    if not letters:
        return ciphertext

    out_letters: list[str] = []
    i = 0
    n = len(letters)
    while i < n:
        block = letters[i:i+period]
        m = len(block)
        coords = [_coords(idx[ch]) for ch in block]

        flat: list[int] = []
        for z, r, c in coords:
            flat.extend((z, r, c))

        Z = flat[:m]
        R = flat[m:2*m]
        C = flat[2*m:3*m]
        for i2 in range(m):
            out_letters.append(alpha[_index(Z[i2], R[i2], C[i2])])
        i += period

    return _reinject(ciphertext, out_letters, meta)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.fractionation.trifid",
        description="Trifid ciphers (3x3x3, A-Z + '.')"
    )

    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("text", help="plaintext/ciphertext (quote if contains spaces)")
    p.add_argument("--key", default="", help="optional key with permutes the A-Z alphabet + '+'.")
    p.add_argument("--period", type=int, default=5, help="block size")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    action = args.action
    text = args.text
    key = args.key
    period = args.period 

    try:
        if action == "encrypt":
            print(encrypt(text, key=key, period=period))
            sys.exit(0)
        elif action == "decrypt":
            print(decrypt(text, key=key, period=period))
            sys.exit(0)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)