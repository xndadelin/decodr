"""
pydecodr.ciphers.classical.atbash - Atbash cipher

Basically each letter is mapped to its reverse counterpard:
A <-> Z, B <-> Y ...
"""

from __future__ import annotations

import argparse
import sys

def _map_char(ch: str) -> str:
    if "a" <= ch <= "z":
        return chr(ord("z") - (ord(ch) - ord("a")))
    if "A" <= ch <= "Z":
        return chr(ord("Z") - (ord(ch) - ord("A")))
    return ch

def transform(text: str) -> str:
    return "".join(_map_char(ch) for ch in text)

def encrypt(text: str) -> str:
    return transform(text)

decrypt = encrypt

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.classical.atbash",
        description="Atbash cipher (encrypt/decrypt)"
    )
    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("text", help="text to process (quote if contains spaces)")
    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    action = args.action
    text = args.text

    try:
        if action in ("encrypt", "decrypt"):
            print(transform(text))
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
