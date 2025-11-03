"""
pydecodr.ciphers.fractionation.nihilist - nihilist cipher
"""

from __future__ import annotations
import sys
import argparse
from typing import List

from pydecodr.ciphers.fractionation.polybius import _build_square, _square_mappings, _clean_plaintext

def _numeric_from_text(text: str, keyword: str, j_as_i: bool = True) -> List[int]:
    square = _build_square(keyword, j_as_i)
    l2c, _ = _square_mappings(square)
    clean = _clean_plaintext(text, j_as_i)
    return [int(f"{l2c[ch][0]}{l2c[ch][1]}") for ch in clean if ch in l2c]

def encrypt(plaintext: str, square_key: str, numeric_key: str, j_as_i: bool = True) -> str:
    nums_text = _numeric_from_text(plaintext, square_key, j_as_i)
    nums_key = _numeric_from_text(numeric_key, square_key, j_as_i)

    out = []
    for i, n in enumerate(nums_text):
        k = nums_key[i % len(nums_key)]
        out.append((n + k) % 100)
    return "".join(f"{v:02d}" for v in out)

def decrypt(ciphertext: str, square_key: str, numeric_key: str, j_as_i: bool = True) -> str:
    ct_pairs = [int(ciphertext[i:i+2]) for i in range(0, len(ciphertext), 2)]
    nums_key = _numeric_from_text(numeric_key, square_key, j_as_i)
    square = _build_square(square_key, j_as_i)
    _, c2l = _square_mappings(square)

    out = []
    for i, n in enumerate(ct_pairs):
        k = nums_key[i % len(nums_key)]
        v = (n - k) % 100
        if 11 <= v <= 55:
            r, c = divmod(v, 10)
            if 1 <= r <= 5 and 1 <= c <= 5:
                out.append(c2l.get((r, c), ""))
    return "".join(out)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.fractionation.nihilist",
        description="Nihilist cipher using polybius square and numeric key"
    )

    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("text", help="Plaintext or ciphertext")
    p.add_argument("square_key", help="Keyword for polybius square (I=J)")
    p.add_argument("numeric_key", help="keyword for numeric key derivation")
    p.add_argument("--no-j-as-i", dest="j_as_i", action="store_false", help="do not merge J into I")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])
    try:
        if args.action == "encrypt":
            print(encrypt(args.text, args.square_key, args.numeric_key, j_as_i=args.j_as_i))
        elif args.action == "decrypt":
            print(decrypt(args.text, args.square_key, args.numeric_key, j_as_i=args.j_as_i))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

