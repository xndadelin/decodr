"""
pydecodr.ciphers.rotor.enigma - its a simplied version for my sake i am not alan turing
"""

from __future__ import annotations
from typing import List
import sys
import argparse

# to do for the the next version: let the user choose its own rotors

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

ROTOR_I = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
ROTOR_II = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
ROTOR_III = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

def _shift_rotor(rotor: str, shift: int) -> str:
    s = shift % 26
    return rotor[s:] + rotor[:s]

def _enc_through_rotor(ch: str, rotor: str) -> str:
    return rotor[ALPHABET.index(ch)]

def _dec_through_rotor(ch: str, rotor: str) -> str:
    return ALPHABET[rotor.index(ch)]

def encrypt(plaintext: str) -> str:
    r1, r2, r3 = ROTOR_I, ROTOR_II, ROTOR_III 
    s1 = s2 = s3 = 0
    out: List[str] = []

    for ch in plaintext.upper():
        if ch not in ALPHABET:
            out.append(ch)
            continue

        s1 = (s1 + 1) % 26
        if s1 == 0:
            s2 = (s2 + 1) % 26
            if s2 == 0:
                s3 = (s3 + 1) % 26
        
        a = _enc_through_rotor(ch, _shift_rotor(r1, s1))
        b = _enc_through_rotor(a, _shift_rotor(r2, s2))
        c = _enc_through_rotor(b, _shift_rotor(r3, s3))

        r = REFLECTOR_B[ALPHABET.index(c)]

        c2 = _dec_through_rotor(r, _shift_rotor(r3, s3))
        b2 = _dec_through_rotor(c2, _shift_rotor(r2, s2))
        a2 = _dec_through_rotor(b2, _shift_rotor(r1, s1))

        out.append(a2)

    return "".join(out)

decrypt = encrypt

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecoder.ciphers.rotor.enigma",
        description="Simplified Enigma cipher - encrypt/decrypt"
    )
    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("text", help="plaintext or ciphertext (quotes if contains spaces)")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    action = args.action
    text = args.text

    try:
        if action == 'encrypt':
            print(encrypt(text))
            sys.exit(0)
        elif action == "decrypt":
            print(decrypt(text))
            sys.exit(0)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f'Error: {e}')