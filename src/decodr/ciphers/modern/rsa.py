"""
decodr.ciphers.modern.rsa - rsa cipher
"""

from __future__ import annotations
from typing import Tuple
import math

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

encode = encrypt
decode = decrypt

if __name__ == "__main__":
    import sys

    usage = (
        "Usage:\n"
        "python3 -m decodr.ciphers.modern.rsa gen <p> <q> [e]\n"
        "python3 -m decodr.ciphers.modern.rsa encrypt <text> <n> <e>\n"
        "python3 -m decodr.ciphers.modern.rsa decrypt <cipher> <n> <d>\n"
    )

    if len(sys.argv) < 3:
        print(usage)
        sys.exit(1)

    cmd = sys.argv[1]
    try:
        if cmd == "gen":
            if len(sys.argv) < 3:
                print("Usage <p> <q> [e]")
                sys.exit(1)
            p, q = int(sys.argv[2]), int(sys.argv[3])
            e = int(sys.argv[4]) if len(sys.argv) >= 5 else 65537
            pub, priv = _generate_keys(p, q, e)
            print(f"Public key (n, e): {pub}")
            print(f"Private key (n, d): {priv}")

        elif cmd in ("encrypt", "encode"):
            if len(sys.argv) < 5:
                print("Usage: encrypt <text> <n> <e>")
                sys.exit(1)
            text, n, e = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
            print(encrypt(text, n, e))
        
        elif cmd in ("decrypt", "decode"):
            if len(sys.argv) < 5:
                print("Usage: decrypt <cipher> <n> <d>")
                sys.exit(1)
            cipher, n, d = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
            print(decrypt(cipher, n, d))

        else:
            print(usage)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


