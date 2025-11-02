"""
pydecodr.ciphers.classical.bacon - bacon cipher (A/B - 5 bit groups)
"""

from __future__ import annotations
import argparse
import string
import sys

ALPH = string.ascii_uppercase

def _bacon_encode_char(ch: str) -> str:
    i = ALPH.index(ch.upper())
    bits = f"{i:05b}"
    return "".join("A" if b == "0" else "B" for b in bits)

def _bacon_decode_group(gr: str) -> str | None:
    if len(gr) != 5:
        return None
    b = []
    for ch in gr:
        if ch.upper() == "A":
            b.append("0")
        elif ch.upper() == "B":
            b.append("1")
        else:
            return None
    val = int("".join(b), 2)
    if 0 <= val < 26:
        return ALPH[val]
    return None

def encrypt(plaintext: str) -> str:
    out = []
    for ch in plaintext:
        if "A" <= ch <= "Z" or "a" <= ch <= "z":
            out.append(_bacon_encode_char(ch))
        else:
            out.append(ch)
    res_parts = []
    for item in out:
        if item and (item[0] in ("A", "B") and (res_parts and res_parts[-1]) and res_parts[-1][-1] in ("A", "B")):
            res_parts.append(" ")
            res_parts.append(item)
        else:
            res_parts.append(item)
    return "".join(res_parts)

def decrypt(ciphertext: str) -> str:
    out = []
    buffer = ""
    for ch in ciphertext:
        if ch.upper() in ("A", "B"):
            buffer += ch.upper()
            if len(buffer) == 5:
                dec = _bacon_decode_group(buffer)
                out.append(dec if dec else "")
                buffer = ""
        else:
            if buffer:
                buffer = ""
            out.append(ch)

    return "".join(out).replace(" ", "")

def _build_argparser() -> argparse.ArgumentParser: 
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.classical.bacon",
        description="Bacon cipher (A/B 5-bit groups)"
    )

    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("text", help="plaintext or ciphertext (quote if contains spaces)")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    action = args.action
    text = args.text

    try:
        if action == "encrypt":
            print(encrypt(text))
            sys.exit(0)
        elif action == "decrypt":
            print(decrypt(text))
            sys.exit(0)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)