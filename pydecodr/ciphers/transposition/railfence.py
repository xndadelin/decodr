"""
pydecodr.ciphers.transposition.railfence - rail fence (zig-zag) ciphers
"""

from __future__ import annotations
import sys
import argparse

def _zigzag_indices(n: int, rails: int) -> list[int]:
    if rails < 2:
        raise ValueError("rails must be >= 2")
    rail = 0
    direction = 1
    rail_of_index: list[int] = []
    for _ in range(n):
        rail_of_index.append(rail)
        rail += direction
        if rail == rails - 1:
            direction = -1
        elif rail == 0:
            direction = 1
    
    indices: list[int] = []
    for r in range(rails):
        indices.extend(i for i, rr in enumerate(rail_of_index) if rr == r)
    return indices

def encrypt(plaintext: str, rails: int = 3) -> str:
    if rails < 2:
        raise ValueError("railst must be >= 2")
    n = len(plaintext)
    order = _zigzag_indices(n, rails)

    return "".join(plaintext[i] for i in order)

def decrypt(ciphertext: str, rails: int = 3) -> str:
    if rails < 2:
        raise ValueError("rails must be >= 2")
    n = len(ciphertext)
    order = _zigzag_indices(n, rails)

    plain = [""] * n
    for k, i in enumerate(order):
        plain[i] = ciphertext[k]

    return "".join(plain[i] for i in range(n))

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.cipherrs.transposition.railfence",
        description="Rail fence cipher"
    )

    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("text", help="plaintext or ciphertext (quote if contains spaces)")
    p.add_argument('--rails', type=int, default=3, help="number of rails")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    action = args.action
    text = args.text
    rails = args.rails

    try:
        if action == "encrypt":
            print(encrypt(text, rails))
            sys.exit(0)
        elif action == "decrypt":
            print(decrypt(text, rails))
            sys.exit(0)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)