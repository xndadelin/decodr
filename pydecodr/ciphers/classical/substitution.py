"""
decodr.ciphers.classical.substitution - simple monoalphabetic substution
"""

from __future__ import annotations
import sys
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

encode = encrypt
decode = decrypt

if __name__ == "__main__":
    usage = (
        "Usage:\n"
        "python3 -m decodr.ciphers.classical.substitution generate-key\n"
        "python3 -m decodr.ciphers.classical.substitution encrypt <text> <key>\n"
        "python3 -m decodr.ciphers.classical.substitution decrypt <text> <key>\n"
    )

    if len(sys.argv) < 2:
        print(usage)
        sys.exit(1)
    
    cmd = sys.argv[1]
    try:
        if cmd == "generate-key":
            print(random_key())
        elif cmd in ("encode", "encrypt"):
            if len(sys.argv) < 4:
                print("encrypt requires <text> <key>")
                sys.exit(1)
            text, key = sys.argv[2], sys.argv[3]
            print(encrypt(text, key))
        elif cmd in ("decrypt", "decode"):
            if len(sys.argv) < 4:
                print("encrypt requires <text> <key>")
                sys.exit(1)
            text, key = sys.argv[2], sys.argv[3]
            print(decrypt(text, key))
        else:
            print("Unknown command.")
            print(usage)
            sys.exit(1)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)
        