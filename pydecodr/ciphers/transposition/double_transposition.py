"""
pydecodr.ciphers.transposition.double_transposition - double columnar transposition
"""

from __future__ import annotations
import sys
import argparse
from math import ceil

def _perm_from_key(key: str) -> list[int]:
    if not key:
        raise ValueError("Key must be not empty!")

    pairs = [(ch, i) for i, ch in enumerate(key)]
    pairs_sorted  = sorted(pairs, key=lambda t: (t[0], t[1]))
    return [i for _, i in pairs_sorted]

def _columnar_encrypt(text: str, key: str, pad: str = "X") -> str:
    w = len(key)
    if w <= 0: 
        raise ValueError("Key length must be >=1 ")
    if len(pad) != 1:
        raise ValueError("Pad must be a single character.")


    perm = _perm_from_key(key)
    

    rem = len(text) % w
    if rem:
        text = text + pad * (w - rem)

    rows = len(text) // w

    out = []
    for col in perm:
        for r in range(rows):
            out.append(text[r * w + col])

    return "".join(out)

def _columnar_decrypt(ct: str, key: str, pad: str | None = None) -> str:
    w = len(key)
    if w <= 0:
        raise ValueError("Key length must be >= 1.")
    
    if len(ct) % w != 0:
        rows = ceil(len(ct) / w)
        fill = pad if (isinstance(pad, str) and len(pad) == 1) else " "
        ct = ct + fill * (rows * w - len(ct))
    else:
        rows = len(ct) // w
        

    perm = _perm_from_key(key)

    columns = [""] * w
    k = 0
    for col in perm:
        columns[col] = ct[k:k + rows]
        k += rows

    out = []
    for r in range(rows):
        for c in range(w):
            out.append(columns[c][r])

    return "".join(out)

def encrypt(plaintext: str, key1: str, key2: str, pad: str = "X") -> str:
    step1 = _columnar_encrypt(plaintext, key1, pad=pad)
    step2 = _columnar_encrypt(step1, key2, pad=pad)
    return step2

def decrypt(ciphertext: str, key1: str, key2: str, pad: str = "X") -> str:
    step1 = _columnar_decrypt(ciphertext, key2, pad=pad).rstrip(pad)
    step2 = _columnar_decrypt(step1, key1, pad=pad).rstrip(pad)
    return step2

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.transposition.double_transposition",
        description="Double columnar transposition (encrypt/decrypt)"
    )

    p.add_argument("action", choices=["encrypt", "decrypt"], help="action")
    p.add_argument("text", help="plaintext/ciphertext (quote if contains spaces)")
    p.add_argument("key1", help="first key (columnn order is lexicographic over chars)")
    p.add_argument("key2", help="second key")
    p.add_argument("--pad", default="X", help="pad character (default: 'X')")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])
    try:
        if args.action == "encrypt":
            print(encrypt(args.text, args.key1, args.key2, pad=args.pad))
            sys.exit(0)
        elif args.action == "decrypt":
            print(decrypt(args.text, args.key1, args.key2, pad=args.pad))
            sys.exit(0)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
