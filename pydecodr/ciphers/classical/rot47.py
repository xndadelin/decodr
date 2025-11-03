"""
pydecodr.ciphers.classical.rot47 - ROT47 over printable ASCII
"""

from __future__ import annotations
import sys
import argparse

_LO = 33
_HI = 126
_SPAN = _HI - _LO + 1
_ROT = 47

def _rot47(ch: str) -> str:
    o = ord(ch)
    if _LO <= o <= _HI:
        return chr(_LO + ((o - _LO + _ROT) % _SPAN))
    return ch

def encrypt(text: str) -> str:
    return "".join(_rot47(c) for c in text)

decrypt = encrypt

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.classical.rot47",
        description="ROT47 cipher"
    )
    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("text", help="plaintext/ciphertext (quote if contains spaces)")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    action = args.action
    text = args.text

    try:
        if action == "encrypt":
            print(encrypt(text))
            sys.exit(0)
        elif action == "decrypt":
            print(decrypt(text))
            sys.exit(0)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
