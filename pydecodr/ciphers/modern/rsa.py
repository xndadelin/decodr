"""
pydecodr.ciphers.modern.rsa - rsa cipher
"""

from __future__ import annotations
from typing import Tuple
import math
import sys
import argparse

def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

def _modinv(a: int, m: int) -> int:
    r0, r1 = a, m
    s0, s1 = 1, 0
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    
    if r0 != 1:
        raise ValueError('Modular inverse does not exist.')

    return s0 % m

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True

def _generate_keys(p: int, q: int, e: int = 65537) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    if p == q:
        raise ValueError("p and q must be distinct primes")
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("p and q must both be primes")
    n = p * q
    phi = (p - 1) * (q - 1)
    if _gcd(e, phi) != 1:
        raise ValueError("e must be coprime with phi(n)")
    
    d = _modinv(e, phi)
    return (n, e), (n, d)

def encrypt(plaintext: str, n: int, e: int) -> str:
    return " ".join(str(pow(ord(ch), e, n)) for ch in plaintext)

def decrypt(ciphertext: str, n: int, d: int) -> str:
    parts = ciphertext.strip().split()
    return "".join(chr(pow(int(x), d, n)) for x in parts)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.modern.rsa",
        description="RSA: keygen, encryptm decrypt"
    )
    sub = p.add_subparsers(dest="command", required=True)

    sp_gen = sub.add_parser("gen", help="generate key from p, q (primes) and optional e")
    sp_gen.add_argument("p", type=int, help="prime p")
    sp_gen.add_argument("q", type=int, help="prime q")
    sp_gen.add_argument("--e", type=int, default=65537, help="public exponent (default: 65537)")

    sp_enc = sub.add_parser("encrypt", help="encrypt text with (n, e)")
    sp_enc.add_argument("text", help="plaintext (quote if contains spaces)")
    sp_enc.add_argument("n", type=int, help="modulus n")
    sp_enc.add_argument("e", type=int, help="public exponent e")

    sp_dec = sub.add_parser("decrypt", help="decrypt cipher with (n, d)")
    sp_dec.add_argument("cipher", help="ciphertext (hex or int string)")
    sp_dec.add_argument("n", type=int, help="modululs n")
    sp_dec.add_argument("d", type=int, help="private exponent d")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    try:
        if args.command == "gen":
            pub, priv = _generate_keys(args.p, args.q, args.e)
            print(f"Public key (n, e): {pub}")
            print(f"Private key (n, d): {priv}")
            sys.exit(0)
        if args.command == "encrypt":
            print(encrypt(args.text, args.n, args.e))
            sys.exit(0)
        
        if args.command == "decrypt":
            print(decrypt(args.cipher, args.n, args.d))
            sys.exit(0)
        
        parser.print_help()
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
