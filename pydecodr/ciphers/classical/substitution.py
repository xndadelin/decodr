"""
pydecodr.ciphers.classical.substitution - simple monoalphabetic substution
"""

from __future__ import annotations
import sys
import argparse
import string
import random
from typing import Tuple, Dict, List

ALPHABET_LO = string.ascii_lowercase
ALPHABET_UP = string.ascii_uppercase

def normalize_key(key: str) -> str:
    return "".join(ch for ch in key if ch.isalpha()).upper()

def validate_key(key: str) -> bool:
    k = normalize_key(key)
    return len(k) == 26 and set(k) == set(ALPHABET_UP)

def random_key() -> str:
    letters = list(ALPHABET_UP)
    random.shuffle(letters)
    return "".join(letters)

def _build_maps(key: str) -> Tuple[Dict[str, str], Dict[str, str]]:
    k = normalize_key(key)
    forward = {ALPHABET_LO[i]: k[i].lower() for i in range(26)}
    forward.update({ALPHABET_UP[i]: k[i] for i in range(26)})
    reverse = { v: u for u, v in forward.items() }
    return forward, reverse

def encrypt(plaintext: str, key: str) -> str:
    if not validate_key(key):
        raise ValueError("Invalid key: must be 26 unique letters A-Z")
    forward, _ = _build_maps(key)
    return "".join(forward.get(ch, ch) for ch in plaintext)

def decrypt(plaintext: str, key: str) -> str:
    if not validate_key(key):
        raise ValueError("Invalid key: must be 26 unique letters A-Z")
    _, reverse = _build_maps(key)
    return "".join(reverse.get(ch, ch) for ch in plaintext)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.classical.substitution",
        description="Monoalphabetic substitution cipher"
    )

    sub = p.add_subparsers(dest="command", required=True)

    sp_gen = sub.add_parser("generate-key", help="generate a random substitution key")
    
    sp_enc = sub.add_parser("encrypt", help="encrypt plaintext with a key")
    sp_enc.add_argument("text", help="plaintext (quote if missing spaces)")
    sp_enc.add_argument("key", help="26-letter key mapping")

    sp_dec = sub.add_parser("decrypt", help="decrypt ciphertext with a key")
    sp_dec.add_argument("text", help="ciphertext (quote if contains spaces)")
    sp_dec.add_argument("key", help="26-letter key mapping")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    try:
        if args.command == "generate-key":
            print(random_key())
            sys.exit(0)
        if args.command == "encrypt":
            print(encrypt(args.text, args.key))
            sys.exit(0)
        if args.command == "decrypt":
            print(decrypt(args.text, args.key))
            sys.exit(0)
        
        parser.print_help()
        sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
