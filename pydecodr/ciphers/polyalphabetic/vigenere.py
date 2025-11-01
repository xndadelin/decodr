"""
pydecodr.ciphers.polyalphabetic.vigenere - Vignere cipher

E_i = (P_i + K_i) mod 26
D_i = (C_i - K_i) mod 26
"""

from __future__ import annotations
import sys
import argparse

def _shift(ch: str, k: int, decrypt: bool = False) -> str:
    if not ch.isalpha():
        return ch
    base = ord("A") if ch.isupper() else ord("a")
    offset = -k if decrypt else k
    return chr((ord(ch) - base + offset) % 26 + base)

def _key_shifts(key: str) -> list[int]:
    return [(ord(c.lower()) - ord("a")) for c in key if c.isalpha()]

def encrypt(plaintext: str, key: str) -> str:
    if not key:
        raise ValueError('Key cannot be empty')
    shifts = _key_shifts(key)
    out = []
    j = 0
    for ch in plaintext:
        if ch.isalpha():
            out.append(_shift(ch, shifts[j % len(shifts)]))
            j += 1
        else:
            out.append(ch)
    return "".join(out)

def decrypt(ciphertext: str, key: str) -> str:
    if not key:
        raise ValueError('Key cannot be empty')
    shifts = _key_shifts(key)
    out = []
    j = 0
    for ch in ciphertext:
        if ch.isalpha():
            out.append(_shift(ch, shifts[j % len(shifts)], decrypt=True))
            j += 1
        else:
            out.append(ch)
    return "".join(out)


def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.polyalphabetic.vigenere",
        description="Vigenere cipher"
    )
    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("text", help="plaintext or ciphertext (quote if contains spaces)")
    p.add_argument("key", help="initial key (strings)")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    action = args.action
    text = args.text
    key = args.key

    try:
        if action == "encrypt":
            print(encrypt(text, key))
            sys.exit(0)
        elif action == "decrypt":
            print(decrypt(text, key))
            sys.exit(0)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)