"""
pydecodr.ciphers.classical.rot13 - ROT13 cipher via caesar(where shift is 13)
"""

from __future__ import annotations
from pydecodr.ciphers.classical import caesar
import sys
import argparse

def encrypt(text: str) -> str:
    return caesar.encrypt(text, shift=13)

def decrypt(text: str) -> str:
    return caesar.decrypt(text, shift=13)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.classical.rot13",
        description="ROT13 cipher (encrypt/decrypt/crack)"
    )
    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("text", help="plaintext or ciphertext (quote if it contains spaces)")
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