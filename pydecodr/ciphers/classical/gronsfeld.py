"""
pydecodr.ciphers.classical.gronsfeld - vigenere with a 0-9 key
"""

from __future__ import annotations
import argparse
import string
import sys

ALPHABET = string.ascii_uppercase
A2I = {c: i for i, c in enumerate(ALPHABET)}
I2A = {i: c for i, c in enumerate(ALPHABET)}

def _digits(key: str) -> list[int]:
    if not key or any(ch not in "0123456789" for ch in key):
        raise ValueError("The Gronsfield key must be a string of numbers")
    return [int(d) for d in key]

def _shift_letter(ch: str, k: int) -> str:
    if "A" <= ch <= "Z":
        return I2A[(A2I[ch] + k) % 26]
    if "a" <= ch <= "z":
        up = ch.upper()
        enc = I2A[(A2I[up] + k) % 26]
        return enc.lower()
    return ch

def _unshift_letter(ch: str, k: int) -> str:
    if "A" <= ch <= "Z":
        return I2A[(A2I[ch] - k) % 26]
    if "a" <= ch <= "z":
        up = ch.upper()
        enc = I2A[(A2I[up] - k) % 26]
        return enc.lower()
    return ch

def encrypt(plaintext: str, key: str) -> str:
    ks = _digits(key)
    out: list[str] = []
    j = 0
    L = len(ks)
    for ch in plaintext:
        if ch.isalpha():
            k = ks[j % L]
            out.append(_shift_letter(ch, k))
            j += 1
        else:
            out.append(ch)
    return "".join(out)


def decrypt(ciphertext: str, key: str) -> str:
    ks = _digits(key)
    out: list[str] = []
    j = 0
    L = len(ks)
    for ch in ciphertext:
        if ch.isalpha():
            k = ks[j % L]
            out.append(_unshift_letter(ch, k))
            j += 1
        else:
            out.append(ch)
    return "".join(out)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.classical.gronsfeld",
        description="Gronsfeld cipher"
    )

    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("text", help="plaintext or ciphertext (quotes if contains spaces)")
    p.add_argument("key", help="numeric key")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    try:
        if args.action == "encrypt":
            print(encrypt(args.text, args.key))
        elif args.action == "decrypt":
            print(decrypt(args.text, args.key))
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)





