"""
pydecodr.ciphers.classical.affine - affine cipher 

Encryption: E(x) = (ax + b) mod 26
Decryption: D(x) = a_inv * (x - b) mod 26
a is the modular inverse of a mod 26
"""
from __future__ import annotations

import sys
import argparse


def _char_to_num(ch: str) -> int:
    return ord(ch.lower()) - ord('a')

def _num_to_char(n: int, upper: bool) -> str:
    base = ord("A") if upper else ord("a")
    return chr((n % 26) + base)

def _modinv(a: int, m: int) -> int:
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"There is no modular inverse for a={a} mod {m}")

def encrypt(plaintext: str, a: int = 5, b: int = 8) -> str:
    result = []
    for ch in plaintext:
        if ch.isalpha() and ch.isascii():
            upper = ch.isupper()
            x = _char_to_num(ch)
            y = (a * x + b) % 26
            result.append(_num_to_char(y, upper))
        else:
            result.append(ch)
    return "".join(result)

def decrypt(ciphertext: str, a: int = 5, b: int = 8) -> str:
    result = []
    a_inv = _modinv(a, 26)
    for ch in ciphertext:
        if ch.isalpha() and ch.isascii():
            upper = ch.isupper()
            y = _char_to_num(ch)
            x = (a_inv * (y - b) % 26)
            result.append(_num_to_char(x, upper))
        else:
            result.append(ch)
    return "".join(result)

encode = encrypt
decode = decrypt

def crack(ciphertex: str) -> list[tuple[int, int, str]]:
    valid_a = [1,3,5,7,9,11,15,17,19,21,23,25]
    results: list[tuple[int, int, str]] = []
    for a in valid_a:
        for b in range(26):
            try:
                pt = decrypt(ciphertex, a, b)
                results.append((a, b, pt))
            except Exception:
                continue
    return results

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.classical.affine",
        description="Affine cipher (encrypt/decrypt/crack)"
    )

    p.add_argument("action", choices=['encrypt', 'decrypt', 'crack'], help="action to perform")
    p.add_argument("text", help="plaintext (for encrypt) or ciphertext (for decrypt/crack)")
    p.add_argument("a", nargs="?", type=int, default=5, help="multiplicative key 'a' (default: 5)")
    p.add_argument("b", nargs="?", type=int, default=8, help="additive key 'b' (default: 8)")
    
    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    action = args.action
    text = args.text
    a = int(args.a) if args.a is not None else 5
    b = int(args.b) if args.b is not None else 8
    
    try:
        if action == "encrypt":
            print(encrypt(text, a, b))
            sys.exit(0)
        elif action == "decrypt":
            print(decrypt(text, a, b))
            sys.exit(0)
        elif action == "crack":
            for a_val, b_val, pt in crack(text):
                print(f"a={a_val:2d}, b={b_val:2d} -> {pt}")
            sys.exit(0)
        else:
            parser.print_help()
            sys.exit(1)
    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)