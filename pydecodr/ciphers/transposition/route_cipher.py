"""
pydecodr.ciphers.transposition.route_cipher - route transposition cipher
"""

from __future__ import annotations
import sys
import argparse
from math import ceil

def _clean_text(text: str) -> str:
    return ''.join(ch.upper() for ch in text if ch.isalnum())

def encrypt(plaintext: str, cols: int, route: str = "cw") -> str:
    text = _clean_text(plaintext)
    rows = ceil(len(text) / cols)
    grid = [['X'] * cols for _ in range(rows)]
    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx < len(text):
                grid[r][c] = text[idx]
                idx += 1
    
    out = []
    if route == "cw":
        for c in range(cols):
            for r in range(rows):
                out.append(grid[r][c])
    elif route == "ccw":
        for c in range(cols -1, -1, -1):
            for r in range(rows - 1, -1, -1):
                out.append(grid[r][c])
    else:
        raise ValueError("Invalid route: must be 'cw' or 'ccw'.")
    
    return ''.join(out)

def decrypt(ciphertext: str, cols: int, route: str = "cw") -> str:
    text = _clean_text(ciphertext)
    rows = ceil(len(text) / cols)
    grid = [[''] * cols for _ in range(rows)]
    idx = 0
    if route == "cw":
        for c in range(cols):
            for r in range(rows):
                if idx < len(text):
                    grid[r][c] = text[idx]
                    idx += 1
    elif route == "ccw":
        for c in range(cols -1, -1, -1):
            for r in range(rows - 1, -1, -1):
                if idx < len(text):
                    grid[r][c] = text[idx]
                    idx += 1
    else:
        raise ValueError("Invalid route: must be 'cw' or 'ccw'.")
    
    out = []
    for r in range(rows):
        for c in range(cols):
            out.append(grid[r][c])
    
    return ''.join(out)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.transposition.route_cipher",
        description="Route transposition cipher"
    )

    p.add_argument("action", choices=["encrypt", 'decrypt'], help="action to perform")
    p.add_argument("text", help="plaintext or ciphertext (quote if contains spaces)")
    p.add_argument("cols", type=int, help="number of columns")
    p.add_argument("--route", default="cw", choices=['cw', 'cww'], help="route direction (the default is cw)")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    try:
        if args.action == "encrypt":
            print(encrypt(args.text, args.col. args.route))
            sys.exit(0)
        elif args.action == "decrypt":
            print(decrypt(args.text, args.col. args.route))
            sys.exit(0)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)



