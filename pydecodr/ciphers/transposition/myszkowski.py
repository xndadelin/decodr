"""
pydecodr.ciphers.transposition.myszkowski - myszkowski transposition cipher
"""

from __future__ import annotations
import sys
import argparse
from math import ceil
from typing import List, Dict

def _build_key_groups(key: str) -> Dict[str, List[int]]:
    groups: Dict[str, List[int]] = {}
    for i, ch in enumerate(key):
        groups.setdefault(ch, []).append(i)
    return groups

def encrypt(plaintext: str, key: str, pad: str = "X") -> str:
    key = key.upper()
    clean = "".join(ch for ch in plaintext.upper() if ch.isalnum())

    w = len(key)
    if w == 0:
        raise ValueError("Key must not be empty.")

    rem = len(clean) % w
    if rem:
        clean += pad * (w - rem)

    rows = len(clean) // w
    groups = _build_key_groups(key)
    sorted_keys = sorted(groups.keys())

    matrix = [list(clean[i * w:(i+1) * w]) for i in range(rows)]

    out = []
    for ch in sorted_keys:
        indices = groups[ch]
        for r in range (rows):
            for c in indices:
                out.append(matrix[r][c])
    
    return "".join(out)

def decrypt(ciphertext: str, key: str, pad: str = "X") -> str:
    key = key.upper()
    w = len(key)

    if w == 0:
        raise ValueError("Key must not be empty.")
    
    groups = _build_key_groups(key)
    sorted_keys = sorted(groups.keys())

    rows = ceil(len(ciphertext) / w)
    matrix = [[""] * w for _ in range(rows)]

    order = []
    for ch in sorted_keys:
        indices = groups[ch]
        for r in range(rows):
            for c in indices:
                order.append((r, c))

    for i, (r, c) in enumerate(order):
        if i < len(ciphertext):
            matrix[r][c] = ciphertext[i]

    out = "".join("".join(row) for row in matrix)
    return out.rstrip(pad)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.transposition.myszkowski",
        description="Myszkowski transposition ciphers"
    )

    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("text", help="plaintext or ciphertext")
    p.add_argument("key", help="keyword")
    p.add_argument("--pad", default="X", help="pad character (default: X)")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])
    try:
        if args.action == "encrypt":
            print(encrypt(args.text, args.key, pad=args.pad))
        elif args.action == "decrypt":
            print(decrypt(args.text, args.key, pad=args.pad))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    
