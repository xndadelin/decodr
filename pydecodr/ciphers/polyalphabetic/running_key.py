"""
pydecodr.ciphers.polyalphabetic.running_key - running-key (book) cipher
"""

from __future__ import annotations
import sys
import argparse
import string

ALPH = string.ascii_uppercase
A2I = {c: i for i, c in enumerate(ALPH)}
I2A = {i: c for i, c in enumerate(ALPH)}

def _only_letters(s: str) -> str:
    return "".join(ch for ch in s.upper() if "A" <= ch <= "Z")

def _require_enough_key(text: str, key: str) -> None:
    letters_in_text = sum(1 for ch in text if ch.isalpha())
    letter_in_key = sum(1 for ch in key if ch.isalpha())
    if letter_in_key < letters_in_text:
        raise ValueError(f"The key must have at least {letters_in_text} letters, but it has {letters_in_text}.")

def encrypt(plaintext: str, keytext: str) -> str:
    _require_enough_key(plaintext, keytext)
    k = _only_letters(keytext)
    out: list[str] = []
    j = 0
    L = len(k)
    for ch in plaintext:
        if ch.isalpha():
            shift = A2I[k[j]]
            if "A" <= ch <= "Z":
                out.append(I2A[(A2I[ch] + shift) % 26])
            else:
                up = ch.upper()
                enc = I2A[(A2I[up] + shift) % 26]
                out.append(enc.lower())
            j += 1
            if j == L:
                j = L - 1
        else:
            out.append(ch)
    return "".join(out)

def decrypt(ciphertext: str, keytext: str) -> str:
    _require_enough_key(ciphertext, keytext)
    k = _only_letters(keytext)
    out: list[str] = []
    j = 0
    L = len(k)
    for ch in ciphertext:
        if ch.isalpha():
            shift = A2I[k[j]]
            if "A" <= ch <= "Z":
                out.append(I2A[(A2I[ch] - shift) % 26])
            else:
                up = ch.upper()
                enc = I2A[(A2I[up] - shift) % 26]
                out.append(enc.lower())
            j += 1
            if j == L:
                j = L - 1
        else:
            out.append(ch)
    return "".join(out)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.polyalphabetic.running_key",
        description="Running-key (book) cipher"
    )
    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("text", help="plaintext/ciphertext (quote if contains spaces)")
    p.add_argument("key", help="long alphabetic key text (e.g., a book passage)")

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
