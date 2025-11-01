"""
pydecodr.ciphers.classical.caesar - Caesar cipher - a monoalphabetic shift

Features:
- encrypt or decript using a integer shift
- non-letters are gonna be preserved as is
"""

from __future__ import annotations

import sys
import argparse

def _shift_char(ch: str, shift: int) -> str:
    if "a" <= ch <= "z":
        base = ord("a")
        return chr((ord(ch) - base + shift) % 26 + base)
    if "A" <= ch <= "Z":
        base = ord("A")
        return chr((ord(ch) - base + shift) % 26 + base)
    return ch

def encrypt(plaintext: str, shift: int = 3) -> str:
    s = shift % 26
    return "".join(_shift_char(ch, s) for ch in plaintext)

def decrypt(ciphertext: str, shift: int = 3) -> str:
    s = (-shift)%26
    return "".join(_shift_char(ch, s) for ch in ciphertext)
    
def crack(ciphertext: str) -> list[tuple[int, str]]:
    results: list[tuple[int, str]] = []
    for sh in range(26):
        pt = decrypt(ciphertext, shift=sh)
        results.append((sh, pt))
    return results

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.classical.caesar",
        description="Caesar cipher (encrypt/decrypt/crack)"
    )
    p.add_argument("action", choices=["encrypt", "decrypt", "crack"], help="action to perform")
    p.add_argument("text", help="plaintext or ciphertext (quote if it contains spaces)")
    p.add_argument("shift", nargs="?", type=int, default=3, help="shift amount (default: 3)")
    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    action = args.action
    text = args.text
    shift = int(args.shift) if args.shift is not None else 3

    try:
        if action == "encrypt":
            print(encrypt(text, shift=shift))
            sys.exit(0)
        elif action == "decrypt":
            print(decrypt(text, shift=shift))
            sys.exit(0)
        elif action == "crack":
            for sh, pt in crack(text):
                print(f"{sh:2d}: {pt}")
            sys.exit(0)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)