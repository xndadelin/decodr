"""
pydecodr.ciphers.polyalphabetic.porta - porta cipher
"""

from __future__ import annotations
import sys
import argparse
import string

ALPH = string.ascii_uppercase
A2I = {c: i for i, c in enumerate(ALPH)}
I2A = {i: c for i, c in enumerate(ALPH)}

def _clean_key(key: str) -> str:
    k = "".join(ch for ch in key.upper() if ch in ALPH)
    if not k:
        raise ValueError("The key must contain at least one alpha letter.")
    return k

def _kindex(kch: str) -> int:
    return A2I[kch] // 2

def _porta_map_index(p_idx: int, kidx: int) -> int:
    if p_idx < 13:
        return 13 + ((p_idx + kidx) % 13)
    else:
        return ((p_idx - 13 - kidx) % 13)

def _map_char(ch: str, kidx: int) -> str:
    if "A" <= ch <= "Z":
        return I2A[_porta_map_index(A2I[ch], kidx)]
    if "a" <= ch <= "z":
        up = ch.upper()
        mapped = I2A[_porta_map_index(A2I[up], kidx)]
        return mapped.lower()
    return ch

def encrypt(plaintext: str, key: str) -> str:
    k = _clean_key(key)
    out = []
    j = 0
    L = len(k)
    for ch in plaintext:
        if ch.isalpha():
            kidx = _kindex(k[j % L])
            out.append(_map_char(ch, kidx))
            j += 1
        else:
            out.append(ch)
    return "".join(out)

def decrypt(ciphertext: str, key: str) -> str:
    return encrypt(ciphertext, key)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.polyalphabetic.porta",
        description="Porta cipher"
    )

    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("text", help="plaintext or ciphertext (quote if contains spaces)")
    p.add_argument("key", help="alphabetic key (A-Z)")

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
